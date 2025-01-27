from utils import load_image

# Параметры модели
LEARNING_RATE = 0.001
GAMMA = 0.99
CLIP_RANGE = 0.2
N_STEPS = 4096
COEF = 0.01
CLIP_RANGE_VF = 0.2
N_EPOCHS = 100
BATCH_SIZE = 64

# Параметры экрана и сетки
SCREEN_SIZE = 550
GRID_SIZE = 11
CELL_SIZE = SCREEN_SIZE // GRID_SIZE

# Параметры игры
BASE_COORD = 5
COUNT_FLOWERS = 10
COUNT_HOLES = 5
MAX_STEPS_GAME = 10000
VIEW_RANGE = 1  # Область зрения 3x3
WATER_CAPACITY = 300  # Максимальный запас воды
ENERGY_CAPACITY = 5000  # Максимальный запас энергии
WATER_CONSUMPTION = 10  # Расход воды на полив
ENERGY_CONSUMPTION_MOVE = 1
ENERGY_CONSUMPTION_WATER = 2
COUNT_ACTIONS = 5
MIN_GAME_STEPS = 2000

# Награды
REWARD_WATER_KNOWN_FLOWER = 2000  # Дополнительное вознаграждение за полив неполитого известного цветка
REWARD_COMPLETION = 10000
REWARD_WATER_SUCCESS = 1500 # Дополнительное вознаграждение за полив неполитого известного цветка
PENALTY_WATER_FAIL_ALREADY_WATERED = -1000  # Если цветок уже полит
PENALTY_WATER_FAIL_NOT_ON_FLOWER = -1500  # Агент попытался полить не находясь на цветке
NEXT_2_UNWATERED_FLOWER = 5  # Вознаграждение за нахождение рядом с неполитым цветком
REWARD_MAX_STEPS_DISTANCE = -10
PENALTY_COLLISION = -1500  # штраф за попадание в яму
REWARD_EXPLORE = 1000  # Вознаграждение за исследование новых клеток
DONT_WATERING = - 500
PENALTY_LOOP = -1500

# Позиции цветов и ям
# PLACEMENT_MODE = 'fixed'
PLACEMENT_MODE = 'random'

FIXED_FLOWER_POSITIONS = [
    (2, 2), (2, 8), (4, 3), (4, 7), (6, 2),
    (6, 8), (8, 4), (8, 6), (3, 5), (7, 5)
]

FIXED_HOLE_POSITIONS = [
    (1, 1), (1, 9), (3, 3), (7, 7), (9, 5)
]

# Цвета, шрифты
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (132, 184, 56)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
FONT_SIZE = 24
TITLE_SIZE = 60

# Подгружаем изображения
AGENT_ICON = load_image("unit.png", CELL_SIZE)  # Изображение робота
FLOWER_ICON = load_image("clumb2.png", CELL_SIZE)  # Сухие цветы
WATERED_FLOWER_ICON = load_image("clumb1.png", CELL_SIZE)  # Политые цветы
HOLE_ICON = load_image("pit.png", CELL_SIZE)  # Яма
BASE_ICON = load_image("robdocst.png", CELL_SIZE)  # База
