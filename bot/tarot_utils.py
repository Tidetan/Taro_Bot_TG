import random

# Пример списка карт Таро
TAROT_CARDS = [
    {"name": "The Fool", "description": "Начало нового пути, новые возможности."},
    {"name": "The Magician", "description": "Сила и способности, использование ресурсов."},
    {"name": "The High Priestess", "description": "Интуиция, внутреннее знание."},
    {"name": "The Empress", "description": "Творчество, изобилие, материнство."},
    {"name": "The Emperor", "description": "Структура, авторитет, контроль."},
    {"name": "The Hierophant", "description": "Традиция, духовное руководство, обучение."},
    {"name": "The Lovers", "description": "Любовь, выбор, гармония."},
    {"name": "The Chariot", "description": "Воля, триумф, контроль над ситуацией."},
    {"name": "Strength", "description": "Сила, мужество, терпение."},
    {"name": "The Hermit", "description": "Уединение, поиск внутреннего света, мудрость."},
    {"name": "Wheel of Fortune", "description": "Судьба, перемены, циклы."},
    {"name": "Justice", "description": "Справедливость, правда, равновесие."},
    {"name": "The Hanged Man", "description": "Жертва, изменение перспективы, подчинение."},
    {"name": "Death", "description": "Конец, трансформация, новое начало."},
    {"name": "Temperance", "description": "Умеренность, баланс, исцеление."},
    {"name": "The Devil", "description": "Материальность, зависимость, искушение."},
    {"name": "The Tower", "description": "Разрушение, откровение, неожиданное изменение."},
    {"name": "The Star", "description": "Надежда, вдохновение, обновление."},
    {"name": "The Moon", "description": "Иллюзии, интуиция, тайны."},
    {"name": "The Sun", "description": "Счастье, успех, радость."},
    {"name": "Judgement", "description": "Суд, возрождение, осознание."},
    {"name": "The World", "description": "Завершение, исполнение, цель."}
]

def get_daily_tarot_card():
    return random.choice(TAROT_CARDS)