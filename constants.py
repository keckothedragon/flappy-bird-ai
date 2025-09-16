DISPLAY_WIDTH: int = 800
DISPLAY_HEIGHT: int = 600

FPS: float = 55.0

ICON_PATH: str = "assets/img/icon.png"

BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
RED: tuple[int, int, int] = (255, 0, 0)
BLUE: tuple[int, int, int] = (0, 0, 255)
GREEN: tuple[int, int, int] = (0, 255, 0)
YELLOW: tuple[int, int, int] = (255, 255, 0)
SKY_BLUE: tuple[int, int, int] = (135, 206, 235)
BG_COLOR: tuple[int, int, int] = SKY_BLUE

PLAYER_START_X: int = 100
PLAYER_START_Y: int = 300
PLAYER_WIDTH: int = 50
PLAYER_HEIGHT: int = 41
PLAYER_JUMP_HEIGHT: int = 10
PLAYER_IMAGES_PATH: list[str] = ["assets/img/player/bird-1.png", "assets/img/player/bird-2.png",
                                 "assets/img/player/bird-3.png", "assets/img/player/bird-2.png"]

PIPE_WIDTH: int = 100
PIPE_GAP_HEIGHT: int = 200
PIPE_IMAGE_PATH: str = "assets/img/pipe/pipe.png"

FLOOR_HEIGHT: int = 50
FLOOR_IMAGE_PATH: str = "assets/img/floor/floor.png"

SCORE_FONT: tuple[str, int] = ("assets/font/flappy-bird-font/flappy-bird-font.ttf", 40)
SCORE_COLOR: tuple[int, int, int] = BLACK

MENU_FONT: tuple[str, int] = ("assets/font/flappybirdy/FlappyBirdy.ttf", 50)
MENU_NUMBER_FONT: tuple[str, int] = ("assets/font/flappy-bird-font/flappy-bird-font.ttf", 30)
MENU_IMAGE_PATH: str = "assets/img/menu/menu.png"
MENU_WIDTH: int = 200
MENU_HEIGHT: int = 300

HIGHSCORE_FILE_PATH = "data/highscore.txt"

FIRST_PLACE_IMAGE_PATH = "assets/img/medals/first.png"
SECOND_PLACE_IMAGE_PATH = "assets/img/medals/second.png"
THIRD_PLACE_IMAGE_PATH = "assets/img/medals/third.png"
PLACEMENT_WIDTH: int = 50
PLACEMENT_HEIGHT: int = 50

PRODUCTION_MODE: int = 0
DEBUG_MODE: int = 1
TRAINING_MODE: int = 2
AUTO_RACE_MODE: int = 3
CURRENT_MODE: int = PRODUCTION_MODE
