from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
from pathlib import Path
import uuid
import os

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "vagzlumauto.db"
UPLOAD_DIR = BASE / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024 * 1024
from config import *

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER,
        price REAL,
        mileage INTEGER,
        power INTEGER,
        fuel TEXT,
        gearbox TEXT,
        body TEXT,
        color TEXT,
        engine TEXT,
        drive TEXT,
        phone TEXT,
        description TEXT,
        vin TEXT,
        owner_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS car_photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER NOT NULL,
        filename TEXT NOT NULL
    );
    """)
    # Додаємо детальні характеристики до вже існуючих баз без втрати даних.
    existing_cols = {r[1] for r in conn.execute("PRAGMA table_info(cars)").fetchall()}
    for field in DETAIL_FIELDS:
        key = field["key"]
        if key not in existing_cols:
            conn.execute(f"ALTER TABLE cars ADD COLUMN {key} TEXT")
    admin_email = os.environ.get("ADMIN_EMAIL", ADMIN_DEFAULT_EMAIL)
    admin_password = os.environ.get("ADMIN_PASSWORD", ADMIN_DEFAULT_PASSWORD)
    existing = conn.execute("SELECT id FROM users WHERE email=?", (admin_email,)).fetchone()
    if not existing:
        conn.execute(
            "INSERT INTO users(email,password_hash,role) VALUES(?,?,?)",
            (admin_email, generate_password_hash(admin_password), "admin")
        )
    conn.commit()
    conn.close()

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    conn = db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    return user

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

def save_upload(file):
    if not file or not file.filename:
        return None
    if not allowed_file(file.filename):
        raise ValueError("Дозволені JPG, JPEG, PNG та WEBP.")
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    file.save(UPLOAD_DIR / filename)
    return filename

def require_role(*roles):
    user = current_user()
    if not user or user["role"] not in roles:
        abort(403)
    return user

@app.context_processor
def inject_globals():
    return {"current_user": current_user(), "roles": ROLES, "site": SITE, "phones": PHONES, "ui": TEXT, "nav": NAV, "detail_field_map": DETAIL_FIELD_MAP, "quick_picker": QUICK_PICKER, "main_fields": MAIN_FIELDS, "detail_fields": DETAIL_FIELDS, "max_photos": MAX_PHOTOS}

@app.route("/")
def home():
    brand = request.args.get("brand", "").strip()
    model = request.args.get("model", "").strip()
    conn = db()
    params = []
    if brand or model:
        sql = """SELECT c.*, (SELECT filename FROM car_photos p WHERE p.car_id=c.id ORDER BY p.id LIMIT 1) AS photo
                 FROM cars c WHERE 1=1"""
        legacy_brand = next((k for k, v in LEGACY_MODEL_BRANDS.items() if v and v.lower() == model.lower()), None) if model else None
        if brand:
            if legacy_brand:
                sql += " AND (LOWER(c.brand)=LOWER(?) OR LOWER(c.brand)=LOWER(?))"
                params.extend([brand, legacy_brand])
            else:
                sql += " AND LOWER(c.brand)=LOWER(?)"
                params.append(brand)
        if model:
            model_condition = "(LOWER(c.model)=LOWER(?) OR LOWER(c.model) LIKE LOWER(?))"
            params.extend([model, model + " %"])
            if legacy_brand and not brand:
                model_condition = f"({model_condition} OR LOWER(c.brand)=LOWER(?))"
                params.append(legacy_brand)
            sql += " AND " + model_condition
        sql += " ORDER BY c.id DESC"
        cars = conn.execute(sql, params).fetchall()
    else:
        cars = conn.execute("""
            SELECT c.*, (SELECT filename FROM car_photos p WHERE p.car_id=c.id ORDER BY p.id LIMIT 1) AS photo
            FROM cars c ORDER BY c.id DESC LIMIT 8
        """).fetchall()
    conn.close()
    return render_template("home.html", cars=cars, selected_brand=brand, selected_model=model,
                           is_filtered=bool(brand or model))

@app.route("/cars")
def cars():
    brand = request.args.get("brand", "").strip()
    model = request.args.get("model", "").strip()
    conn = db()
    sql = """SELECT c.*, (SELECT filename FROM car_photos p WHERE p.car_id=c.id ORDER BY p.id LIMIT 1) AS photo
             FROM cars c WHERE 1=1"""
    params = []
    if brand:
        sql += " AND LOWER(c.brand)=LOWER(?)"
        params.append(brand)
    if model:
        sql += " AND (LOWER(c.model)=LOWER(?) OR LOWER(c.model) LIKE LOWER(?))"
        params.extend([model, model + " %"])
    sql += " ORDER BY c.id DESC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return render_template("cars.html", cars=rows, brands=CAR_BRANDS, models=CAR_MODELS,
                           selected_brand=brand, selected_model=model)

@app.route("/cars/<int:car_id>")
def car_detail(car_id):
    conn = db()
    car = conn.execute("SELECT * FROM cars WHERE id=?", (car_id,)).fetchone()
    photos = conn.execute("SELECT * FROM car_photos WHERE car_id=? ORDER BY id", (car_id,)).fetchall()
    conn.close()
    if not car:
        abort(404)
    return render_template("car_detail.html", car=car, photos=photos, detail_groups=DETAIL_GROUPS)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not email or len(password) < 6:
            flash("Вкажіть email та пароль мінімум із 6 символів.", "error")
            return redirect(url_for("register"))
        conn = db()
        try:
            cur = conn.execute(
                "INSERT INTO users(email,password_hash,role) VALUES(?,?,?)",
                (email, generate_password_hash(password), "user")
            )
            conn.commit()
            session["user_id"] = cur.lastrowid
            flash("Реєстрація успішна. Зараз у вас звичайні права користувача.", "success")
            return redirect(url_for("home"))
        except sqlite3.IntegrityError:
            flash("Такий email уже зареєстрований.", "error")
        finally:
            conn.close()
    return render_template("auth.html", mode="register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        conn = db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            flash("Ви увійшли на сайт.", "success")
            return redirect(url_for("home"))
        flash("Невірний email або пароль.", "error")
    return render_template("auth.html", mode="login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/admin/users")
def admin_users():
    require_role("admin")
    conn = db()
    users = conn.execute("SELECT id,email,role,created_at FROM users ORDER BY id").fetchall()
    conn.close()
    return render_template("admin_users.html", users=users)

@app.route("/admin/users/<int:user_id>/role", methods=["POST"])
def change_role(user_id):
    require_role("admin")
    role = request.form.get("role")
    if role not in ROLES:
        abort(400)
    conn = db()
    conn.execute("UPDATE users SET role=? WHERE id=?", (role, user_id))
    conn.commit()
    conn.close()
    flash("Права користувача змінено.", "success")
    return redirect(url_for("admin_users"))

@app.route("/admin/cars/new", methods=["GET", "POST"])
def add_car():
    user = require_role("editor", "admin")
    defaults = {"brand":"", "model":"", "year":"", "price":"", "mileage":"", "power":"",
                "fuel":"", "gearbox":"", "body":"", "color":"", "engine":"", "drive":"",
                "phone":"", "description":"", "vin":""}
    defaults.update({field["key"]: "" for field in DETAIL_FIELDS})
    detail_values = {field["key"]: "" for field in DETAIL_FIELDS}

    if request.method == "POST":
        fields = {key: request.form.get(key, "").strip() for key in defaults}
        if not fields["brand"] or not fields["model"]:
            flash("Марка та модель є обов'язковими.", "error")
            return render_template("car_form.html", **fields, brands=CAR_BRANDS, models=CAR_MODELS,
                                   fuel_options=FUEL, gearbox_options=GEARBOX, body_options=BODY,
                                   drive_options=DRIVE, existing_cars=get_existing_cars(), detail_values={k: fields.get(k, "") for k in DETAIL_FIELD_MAP})
        conn = db()
        cur = conn.execute("""
            INSERT INTO cars(brand,model,year,price,mileage,power,fuel,gearbox,body,color,engine,drive,phone,description,vin,owner_id,
            generation,trim,modification,eco_standard,condition,fuel_consumption,safety,air_conditioner,comfort,optics,multimedia,interior_body,headlights,parking,airbags)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, tuple(fields[k] if k not in {"owner_id"} else fields[k] for k in []) +
             (fields["brand"], fields["model"], fields["year"] or None, fields["price"] or None, fields["mileage"] or None,
              fields["power"] or None, fields["fuel"], fields["gearbox"], fields["body"], fields["color"], fields["engine"],
              fields["drive"], fields["phone"], fields["description"], fields["vin"], user["id"],
              *(fields[f["key"]] for f in DETAIL_FIELDS)))
        car_id = cur.lastrowid
        photo_files = [f for f in request.files.getlist("photos") if f and f.filename]
        if len(photo_files) > MAX_PHOTOS:
            conn.rollback(); conn.close()
            flash(f"Можна додати максимум {MAX_PHOTOS} фото до одного авто.", "error")
            return render_template("car_form.html", **fields, brands=CAR_BRANDS, models=CAR_MODELS,
                                   fuel_options=FUEL, gearbox_options=GEARBOX, body_options=BODY,
                                   drive_options=DRIVE, existing_cars=get_existing_cars(), detail_values={k: fields.get(k, "") for k in DETAIL_FIELD_MAP})
        saved_files = []
        try:
            for f in photo_files:
                filename = save_upload(f)
                if filename:
                    saved_files.append(filename)
                    conn.execute("INSERT INTO car_photos(car_id,filename) VALUES(?,?)", (car_id, filename))
        except ValueError as exc:
            conn.rollback()
            for filename in saved_files: (UPLOAD_DIR / filename).unlink(missing_ok=True)
            conn.close()
            flash(str(exc), "error")
            return render_template("car_form.html", **fields, brands=CAR_BRANDS, models=CAR_MODELS,
                                   fuel_options=FUEL, gearbox_options=GEARBOX, body_options=BODY,
                                   drive_options=DRIVE, existing_cars=get_existing_cars(), detail_values={k: fields.get(k, "") for k in DETAIL_FIELD_MAP})
        conn.commit(); conn.close()
        flash("Автомобіль додано.", "success")
        return redirect(url_for("add_car"))

    return render_template("car_form.html", **defaults, brands=CAR_BRANDS, models=CAR_MODELS,
                           fuel_options=FUEL, gearbox_options=GEARBOX, body_options=BODY,
                           drive_options=DRIVE, existing_cars=get_existing_cars(), detail_values=detail_values)


@app.route("/admin/cars/<int:car_id>/edit", methods=["GET", "POST"])
def edit_car(car_id):
    user = require_role("editor", "admin")
    conn = db()
    car = conn.execute("SELECT * FROM cars WHERE id=?", (car_id,)).fetchone()
    photos = conn.execute("SELECT * FROM car_photos WHERE car_id=? ORDER BY id", (car_id,)).fetchall()
    conn.close()
    if not car:
        abort(404)

    fields = {key: (car[key] if key in car.keys() else "") for key in [
        "brand", "model", "year", "price", "mileage", "power", "fuel", "gearbox", "body", "color", "engine", "drive",
        "phone", "description", "vin", *(f["key"] for f in DETAIL_FIELDS)
    ]}
    detail_values = {f["key"]: fields.get(f["key"], "") for f in DETAIL_FIELDS}

    if request.method == "POST":
        fields = {key: request.form.get(key, "").strip() for key in fields}
        detail_values = {f["key"]: fields.get(f["key"], "") for f in DETAIL_FIELDS}
        if not fields["brand"] or not fields["model"]:
            flash("Марка та модель є обов'язковими.", "error")
        else:
            conn = db()
            conn.execute("""
                UPDATE cars SET brand=?,model=?,year=?,price=?,mileage=?,power=?,fuel=?,gearbox=?,body=?,color=?,engine=?,drive=?,phone=?,description=?,vin=?,
                generation=?,trim=?,modification=?,eco_standard=?,condition=?,fuel_consumption=?,safety=?,air_conditioner=?,comfort=?,optics=?,multimedia=?,interior_body=?,headlights=?,parking=?,airbags=?
                WHERE id=?
            """, (
                fields["brand"], fields["model"], fields["year"] or None, fields["price"] or None, fields["mileage"] or None,
                fields["power"] or None, fields["fuel"], fields["gearbox"], fields["body"], fields["color"], fields["engine"],
                fields["drive"], fields["phone"], fields["description"], fields["vin"], *(fields[f["key"]] for f in DETAIL_FIELDS), car_id
            ))
            photo_files = [f for f in request.files.getlist("photos") if f and f.filename]
            current_count = conn.execute("SELECT COUNT(*) FROM car_photos WHERE car_id=?", (car_id,)).fetchone()[0]
            if current_count + len(photo_files) > MAX_PHOTOS:
                conn.rollback(); conn.close()
                flash(f"Можна мати максимум {MAX_PHOTOS} фото до одного авто.", "error")
                return render_template("car_form.html", **fields, brands=CAR_BRANDS, models=CAR_MODELS,
                    fuel_options=FUEL, gearbox_options=GEARBOX, body_options=BODY, drive_options=DRIVE,
                    existing_cars=get_existing_cars(), detail_values=detail_values, edit_mode=True, edit_car_id=car_id, edit_photos=photos)
            saved_files = []
            try:
                for f in photo_files:
                    filename = save_upload(f)
                    if filename:
                        saved_files.append(filename)
                        conn.execute("INSERT INTO car_photos(car_id,filename) VALUES(?,?)", (car_id, filename))
            except ValueError as exc:
                conn.rollback()
                for filename in saved_files: (UPLOAD_DIR / filename).unlink(missing_ok=True)
                conn.close()
                flash(str(exc), "error")
                return render_template("car_form.html", **fields, brands=CAR_BRANDS, models=CAR_MODELS,
                    fuel_options=FUEL, gearbox_options=GEARBOX, body_options=BODY, drive_options=DRIVE,
                    existing_cars=get_existing_cars(), detail_values=detail_values, edit_mode=True, edit_car_id=car_id, edit_photos=photos)
            conn.commit()
            conn.close()
            flash("Автомобіль оновлено.", "success")
            return redirect(url_for("edit_car", car_id=car_id))

    return render_template("car_form.html", **fields, brands=CAR_BRANDS, models=CAR_MODELS,
        fuel_options=FUEL, gearbox_options=GEARBOX, body_options=BODY, drive_options=DRIVE,
        existing_cars=get_existing_cars(), detail_values=detail_values, edit_mode=True, edit_car_id=car_id, edit_photos=photos)

@app.route("/admin/cars/<int:car_id>/photos/<int:photo_id>/delete", methods=["POST"])
def delete_car_photo(car_id, photo_id):
    require_role("editor", "admin")
    conn = db()
    photo = conn.execute("SELECT filename FROM car_photos WHERE id=? AND car_id=?", (photo_id, car_id)).fetchone()
    if not photo:
        conn.close()
        abort(404)
    conn.execute("DELETE FROM car_photos WHERE id=? AND car_id=?", (photo_id, car_id))
    conn.commit()
    conn.close()
    try:
        (UPLOAD_DIR / photo["filename"]).unlink(missing_ok=True)
    except OSError:
        pass
    flash("Фото видалено.", "success")
    return redirect(url_for("edit_car", car_id=car_id))

def get_existing_cars():
    conn = db()
    rows = conn.execute("""SELECT c.*, (SELECT filename FROM car_photos p WHERE p.car_id=c.id ORDER BY p.id LIMIT 1) AS photo,
                          (SELECT COUNT(*) FROM car_photos p WHERE p.car_id=c.id) AS photo_count
                          FROM cars c ORDER BY c.id DESC""").fetchall()
    conn.close()
    return rows

@app.route("/admin/cars/<int:car_id>/delete", methods=["POST"])
def delete_car(car_id):
    require_role("editor", "admin")
    conn = db()
    photos = conn.execute("SELECT filename FROM car_photos WHERE car_id=?", (car_id,)).fetchall()
    conn.execute("DELETE FROM car_photos WHERE car_id=?", (car_id,))
    conn.execute("DELETE FROM cars WHERE id=?", (car_id,))
    conn.commit()
    conn.close()
    for p in photos:
        try:
            (UPLOAD_DIR / p["filename"]).unlink(missing_ok=True)
        except OSError:
            pass
    flash("Оголошення видалено.", "success")
    return redirect(url_for("cars"))

@app.route("/parts")
def parts():
    return render_template("contact_service.html", page="Запчастини", icon="🔧", color="orange",
                           text="У нас є запчастини з розборки та нові деталі для GOLF, JETTA, NISSAN, PASSAT, RENAULT і TOURAN.")

@app.route("/repair")
def repair():
    return render_template("repair.html", services=SERVICES)

@app.route("/wheels")
def wheels():
    return render_template("contact_service.html", page="Колеса та диски", icon="◉", color="blue",
                           text="Б/у колеса, диски та титани. Підберемо комплект під ваш автомобіль.")

@app.route("/additional")
def additional():
    return render_template("additional.html", services=ADDITIONAL_SERVICES)

@app.route("/additional/<slug>")
def additional_detail(slug):
    service = next((item for item in ADDITIONAL_SERVICES if item["slug"] == slug), None)
    if not service:
        abort(404)
    return render_template("additional_detail.html", service=service)

@app.route("/admin")
def admin():
    require_role("admin")
    conn = db()
    users_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    cars_count = conn.execute("SELECT COUNT(*) FROM cars").fetchone()[0]
    editors_count = conn.execute("SELECT COUNT(*) FROM users WHERE role='editor'").fetchone()[0]
    conn.close()
    return render_template("admin.html", users_count=users_count, cars_count=cars_count, editors_count=editors_count)

init_db()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
        use_reloader=False,
        threaded=True
    )