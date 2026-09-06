# ============================================================
# VagZlumAuto — ВСІ НАЛАШТУВАННЯ САЙТУ В ОДНОМУ ФАЙЛІ
#
# Тут можна змінювати тексти, контакти, марки, моделі, поля
# форми, кузови, паливо, послуги, меню та зовнішні написи.
# Після змін збережи файл і перезапусти app.py.
# ============================================================

SITE = {
    "name": "VagZlumAuto",
    "title": "Авто в Сокалі",
    "city": "Сокаль",
    "region": "Львівська область",
    "address": "м. Сокаль, вул. Татаркавська",
    "working_hours": "Пн–Сб: 09:00–18:00",
    "working_hours_note": "Неділя — за домовленістю",
    "footer": "Авто, запчастини, ремонт та колеса у Сокалі та Львівській області.",
    "hero_badge": "Авто, запчастини, ремонт та колеса у Сокалі",
    "hero_title": "Авто в Сокалі",
    "hero_text": "Продаж вживаних авто: TOURAN, GOLF, JETTA, PASSAT, RENAULT, FORD, DACIA, NISSAN.",
    "hero_subtext": "Сервіс, ремонт, б/у запчастини та б/у колеса.",
    "currency_symbol": "$",
    "currency_name": "доларів США",
    "currency_position": "after",  # before / after
}

# ------------------------------------------------------------
# КОНТАКТИ — ці номери використовуються всіма кнопками дзвінка
# ------------------------------------------------------------
PHONES = [
    {"display": "+380 63 956 5333", "digits": "380639565333"},
    {"display": "+380 99 956 5333", "digits": "380999565333"},
    {"display": "+380 98 956 5333", "digits": "380989565333"},
]

# ------------------------------------------------------------
# МЕНЮ
# key = внутрішній маршрут, name = напис у меню
# ------------------------------------------------------------
NAV = [
    {"key": "home", "name": "Головна", "endpoint": "home"},
    {"key": "cars", "name": "Підібрати авто", "endpoint": "cars"},
    {"key": "parts", "name": "Запчастини", "endpoint": "parts"},
    {"key": "repair", "name": "Ремонт", "endpoint": "repair"},
    {"key": "wheels", "name": "Колеса", "endpoint": "wheels"},
    {"key": "additional", "name": "Додатково", "endpoint": "additional"},
    {"key": "add_car", "name": "Додати", "endpoint": "add_car", "roles": ["editor", "admin"]},
    {"key": "admin_users", "name": "Користувачі", "endpoint": "admin_users", "roles": ["admin"]},
]

# ------------------------------------------------------------
# МАРКИ ТА ВСІ МОДЕЛІ
# Додавай нову марку одним ключем і список її моделей нижче.
# ------------------------------------------------------------
CAR_MODELS = {
    "Volkswagen": [
        "Golf", "Golf 1.0 TSI", "Golf 1.2 TSI", "Golf 1.4 TSI", "Golf 1.5 TSI", "Golf 1.5 eTSI",
        "Golf 1.6", "Golf 1.6 TDI", "Golf 2.0", "Golf 2.0 TDI", "Golf 2.0 TSI", "Golf 2.0 GTI", "Golf R", "Golf GTE",
        "Jetta", "Jetta 1.4 TSI", "Jetta 1.6", "Jetta 1.8 TSI", "Jetta 2.0", "Jetta 2.0 TDI", "Jetta GLI",
        "Passat", "Passat 1.4 TSI", "Passat 1.5 TSI", "Passat 1.8 TSI", "Passat 2.0 TSI", "Passat 2.0 TDI", "Passat 2.0 BiTDI", "Passat GTE",
        "Touran", "Touran 1.2 TSI", "Touran 1.4 TSI", "Touran 1.6 TDI", "Touran 2.0 TDI",
    ],
    "Renault": [
        "Clio", "Megane", "Laguna", "Scenic", "Espace", "Talisman", "Captur", "Kadjar", "Koleos", "Austral", "Arkana", "Kangoo", "Trafic", "Master", "Zoe", "Duster"
    ],
    "Ford": [
        "Fiesta", "Focus", "Mondeo", "Fusion", "Taurus", "Mustang", "Puma", "Kuga", "Edge", "Explorer", "Escape", "Bronco", "Bronco Sport", "Expedition", "EcoSport", "Maverick", "Ranger", "F-150", "F-250", "F-350", "Transit", "Transit Custom", "Transit Connect", "Transit Courier", "Tourneo Connect", "Tourneo Custom", "Galaxy", "S-Max", "C-Max", "Grand C-Max", "B-Max", "Ka", "Ka+", "Crown Victoria", "GT", "GT40", "Probe", "Capri", "Escort", "Sierra", "Scorpio", "Granada", "Orion", "Puma ST", "Focus ST", "Focus RS", "Fiesta ST", "Mustang Mach-E"
    ],
    "Dacia": [
        "Logan", "Sandero", "Sandero Stepway", "Duster", "Jogger", "Spring", "Lodgy", "Dokker", "Dokker Van", "Logan MCV", "Logan Pick-Up", "Solenza", "1310", "Bigster"
    ],
    "Nissan": [
        "Almera", "Juke", "Micra", "Navara", "Note", "Qashqai", "X-Trail", "Leaf", "Murano", "Pathfinder", "Primera", "Tiida"
    ],
}
CAR_BRANDS = list(CAR_MODELS.keys())

# Швидкі картки на сторінці «Підібрати авто».
# type=model — показує конкретну модель Volkswagen; type=brand — всю марку.
QUICK_PICKER = [
    {"title": "GOLF", "brand": "Volkswagen", "model": "Golf", "type": "model"},
    {"title": "JETTA", "brand": "Volkswagen", "model": "Jetta", "type": "model"},
    {"title": "PASSAT", "brand": "Volkswagen", "model": "Passat", "type": "model"},
    {"title": "TOURAN", "brand": "Volkswagen", "model": "Touran", "type": "model"},
    {"title": "RENAULT", "brand": "Renault", "model": "", "type": "brand"},
    {"title": "FORD", "brand": "Ford", "model": "", "type": "brand"},
    {"title": "DACIA", "brand": "Dacia", "model": "", "type": "brand"},
]

# ------------------------------------------------------------
# ВАРІАНТИ ФОРМИ ДОДАВАННЯ АВТО
# ------------------------------------------------------------
FUEL = ["Бензин", "Дизель", "Гібрид", "Електро", "Газ/бензин", "Водень"]
GEARBOX = ["Механіка", "Автомат", "DSG", "Варіатор", "Робот"]
BODY = [
    "Седан", "Хетчбек", "Універсал", "Купе", "Кабріолет", "Ліфтбек", "Фастбек", "Тарга", "Родстер",
    "Кросовер", "Позашляховик", "Мінівен", "Мікроавтобус", "Фургон", "Пікап", "Універсал/фургон", "Компактвен"
]
DRIVE = ["Передній", "Задній", "Повний"]

# Поля основної інформації: name, key, type, required, placeholder.
MAIN_FIELDS = [
    {"key": "brand", "name": "Марка", "type": "select", "required": True},
    {"key": "model", "name": "Модель", "type": "select", "required": True},
    {"key": "year", "name": "Рік", "type": "number", "required": True, "placeholder": "2021"},
    {"key": "price", "name": "Ціна, $", "type": "number", "required": True, "placeholder": "25000"},
    {"key": "mileage", "name": "Пробіг, тис. км", "type": "number", "placeholder": "226"},
    {"key": "fuel", "name": "Паливо", "type": "select"},
    {"key": "gearbox", "name": "Коробка", "type": "select"},
    {"key": "body", "name": "Кузов", "type": "select"},
    {"key": "color", "name": "Колір", "type": "text", "placeholder": "Чорний"},
    {"key": "engine", "name": "Двигун", "type": "text", "placeholder": "2.0 л"},
    {"key": "drive", "name": "Привід", "type": "select"},
    {"key": "phone", "name": "Телефон", "type": "text", "placeholder": "+380...", "full": True},
    {"key": "description", "name": "Опис", "type": "textarea", "placeholder": "Опис автомобіля...", "full": True},
    {"key": "vin", "name": "VIN", "type": "text", "placeholder": "VIN-код автомобіля", "full": True},
]

# Детальні характеристики — ці назви і підказки можна повністю міняти тут.
DETAIL_FIELDS = [
    {"key": "generation", "name": "Покоління", "placeholder": "Mk7"},
    {"key": "trim", "name": "Комплектація", "placeholder": "Highline / GTI / Business"},
    {"key": "modification", "name": "Модифікація", "placeholder": "2.0 TSI 245 к.с."},
    {"key": "eco_standard", "name": "Екологічний стандарт", "placeholder": "Євро 6"},
    {"key": "condition", "name": "Стан", "placeholder": "Не битий, не фарбований"},
    {"key": "fuel_consumption", "name": "Витрати пального (л/100км)", "placeholder": "7.0 місто / 5.0 траса"},
    {"key": "safety", "name": "Безпека (через кому)", "placeholder": "ABS, ESP, ASR, EBD", "full": True},
    {"key": "air_conditioner", "name": "Кондиціонер (через кому)", "placeholder": "Клімат-контроль, кондиціонер", "full": True},
    {"key": "comfort", "name": "Комфорт (через кому)", "placeholder": "Підігрів сидінь, круїз-контроль", "full": True},
    {"key": "optics", "name": "Оптика (через кому)", "placeholder": "LED фари, ДХВ", "full": True},
    {"key": "multimedia", "name": "Мультимедіа (через кому)", "placeholder": "Apple CarPlay, Android Auto, Bluetooth", "full": True},
    {"key": "interior_body", "name": "Матеріали салону (через кому)", "placeholder": "Шкіряний салон, алюмінієві вставки", "full": True},
    {"key": "headlights", "name": "Фари (через кому)", "placeholder": "LED, автоматичне включення", "full": True},
    {"key": "parking", "name": "Система допомоги при паркуванні (через кому)", "placeholder": "Парктроніки передні/задні, камера", "full": True},
    {"key": "airbags", "name": "Подушки безпеки (через кому)", "placeholder": "Фронтальні, бічні, занавіски", "full": True},
]
DETAIL_FIELD_MAP = {x["key"]: x for x in DETAIL_FIELDS}

# ------------------------------------------------------------
# ДОДАТКОВІ ПОСЛУГИ
# ------------------------------------------------------------
ADDITIONAL_SERVICES = [
    {"slug": "shinomontazh", "name": "Шиномонтаж", "icon": "◉", "description": "Монтаж та демонтаж шин, балансування коліс, перевірка тиску та підготовка автомобіля до сезону."},
    {"slug": "himchistka", "name": "Хімчистка", "icon": "✦", "description": "Професійна хімчистка салону автомобіля: сидіння, стеля, підлога, пластик та важкодоступні місця."},
    {"slug": "myika-avto", "name": "Мийка авто", "icon": "✧", "description": "Комплексна мийка автомобіля з очищенням кузова, скла та коліс. Доступні різні варіанти миття."},
    {"slug": "detailing", "name": "Детейлінг", "icon": "◆", "description": "Детейлінг кузова та салону: глибоке очищення, відновлення зовнішнього вигляду та захист поверхонь."},
    {"slug": "computer-diagnostics", "name": "Компʼютерна діагностика", "icon": "⚡", "description": "Компʼютерна перевірка електронних блоків автомобіля, зчитування помилок та діагностика несправностей."},
    {"slug": "prygon-avto", "name": "Пригон авто", "icon": "➜", "description": "Допоможемо підібрати та пригнати автомобіль під ваш бюджет і побажання, перевіримо варіанти перед купівлею."},
]

SERVICES = [
    ("Заміна масла та фільтрів", "Регулярне ТО та заміна витратних матеріалів.", "від 800 грн"),
    ("Діагностика двигуна", "Комп'ютерна та механічна діагностика.", "від 500 грн"),
    ("Ремонт гальмівної системи", "Колодки, диски, супорти та гальмівна рідина.", "від 1 500 грн"),
    ("Ремонт підвіски", "Діагностика та заміна елементів ходової.", "від 2 000 грн"),
    ("Ремонт та заміна двигуна", "Ремонтні роботи та заміна агрегатів.", "від 15 000 грн"),
    ("Ремонт коробки передач", "Механічні та автоматичні КПП.", "від 8 000 грн"),
    ("Електрика та діагностика", "Пошук і усунення електричних несправностей.", "від 600 грн"),
    ("Ремонт кондиціонера", "Заправка, діагностика та ремонт системи.", "від 600 грн"),
    ("Ремонт вихлопної системи", "Глушник, каталізатор та інші елементи.", "від 2 500 грн"),
    ("Комп'ютерна діагностика", "Повна перевірка електронних блоків автомобіля.", "від 400 грн"),
]

# ------------------------------------------------------------
# УСІ НАПИСИ І ПОВІДОМЛЕННЯ САЙТУ
# ------------------------------------------------------------
TEXT = {
    "nav_call": "☎ Зателефонувати",
    "nav_login": "Увійти",
    "nav_logout": "Вийти",
    "call_title": "Зателефонуйте нам",
    "call_subtitle": "Оберіть зручний номер для зв’язку",
    "viber": "◯ Вайбер",
    "telegram": "➤ Телеграм",
    "close": "Закрити",
    "catalog": "Каталог",
    "pick_title": "Підібрати авто",
    "pick_subtitle": "Оберіть марку та модель автомобіля",
    "show_cars": "Показати авто ›",
    "show_all": "Показати всі авто ›",
    "all_cars": "Всі авто ›",
    "recommended": "Рекомендовані авто",
    "recommended_subtitle": "Найкращі пропозиції у Сокалі",
    "recommended_badge": "Рекомендуємо",
    "details": "Детальніше ›",
    "back_to_picker": "← Повернутися до підбору",
    "change_selection": "Змінити вибір ›",
    "filter_note": "Показуємо лише автомобілі за вашим вибором",
    "empty_filter_title": "Такого автомобіля зараз немає",
    "empty_filter_text": "Автомобілів за вашим вибором не знайдено. Зателефонуйте нам — допоможемо знайти потрібну машину.",
    "empty_cars": "Поки що автомобілів немає.",
    "price_request": "Ціна за запитом",
    "year": "рік",
    "thousand_km": "тис. км",
    "call_us": "☎ Зателефонувати нам",
    "detail_back": "← Назад до списку",
    "detail_characteristics": "Характеристики",
    "detail_description": "Опис",
    "no_description": "Опис автомобіля не додано.",
    "interested": "Зацікавило це авто?",
    "interested_text": "Зателефонуйте нам, щоб дізнатися більше та домовитися про огляд у Львові.",
    "form_panel": "Панель редактора",
    "add_car": "Додати автомобіль",
    "edit_car": "Редагувати автомобіль",
    "add_hint": "Заповніть характеристики та додайте фото.",
    "edit_hint": "Змініть характеристики, додайте нові фото або видаліть непотрібні.",
    "main_info": "Основна інформація",
    "choose_brand": "Оберіть марку",
    "choose_model": "Оберіть модель",
    "empty_option": "—",
    "detail_info": "Детальні характеристики",
    "photos": "Фото",
    "added_photos": "Додані фото",
    "new_photos": "Додати нові фото",
    "photo_choose": "Оберіть фото з телефону або ПК",
    "photo_hint": "Можна додати максимум 100 фото до одного автомобіля.",
    "photo_edit_hint": "Можна додати нові фото, якщо загальна кількість не перевищить 100.",
    "delete_photo": "Видалити фото",
    "save_changes": "Зберегти зміни",
    "publish_car": "Опублікувати авто",
    "existing_cars": "Існуючі авто",
    "edit": "Редагувати",
    "delete": "Видалити",
    "admin_details": "Детальніше",
    "confirm_delete_photo": "Видалити це фото?",
    "confirm_delete_car": "Видалити це авто?",
    "parts_text": "У нас є запчастини з розборки та нові деталі для GOLF, JETTA, PASSAT, RENAULT, FORD, DACIA, NISSAN і TOURAN.",
    "wheels_text": "Б/у колеса, диски та титани. Підберемо комплект під ваш автомобіль.",
    "no_match_call": "Якщо потрібної машини немає — зателефонуйте нам, і ми допоможемо з пошуком.",
}

# Заголовки блоків на сторінці детального авто.
DETAIL_GROUPS = [
    ("Безпека", "safety"),
    ("Кондиціонер", "air_conditioner"),
    ("Комфорт", "comfort"),
    ("Оптика", "optics"),
    ("Мультимедіа", "multimedia"),
    ("Салон та кузов", "interior_body"),
    ("Фари", "headlights"),
    ("Система допомоги при паркуванні", "parking"),
    ("Подушка безпеки", "airbags"),
]

# ------------------------------------------------------------
# РОЛІ / ФОТО / БАЗА
# ------------------------------------------------------------
ROLES = {"user": "Користувач", "editor": "Редактор", "admin": "Адміністратор"}
MAX_PHOTOS = 100
ALLOWED = {"jpg", "jpeg", "png", "webp"}
ADMIN_DEFAULT_EMAIL = "admin@vagzlumauto.local"
ADMIN_DEFAULT_PASSWORD = "Admin123!"

# Старі записи бази, створені до схеми Марка -> Модель.
LEGACY_MODEL_BRANDS = {
    "GOLF": "Golf", "JETTA": "Jetta", "PASSAT": "Passat", "TOURAN": "Touran",
    "RENAULT": None, "FORD": None, "DACIA": None,
}

# Необов'язкові стартові автомобілі. Працюють тільки якщо база порожня.
DEMO_CARS = []
