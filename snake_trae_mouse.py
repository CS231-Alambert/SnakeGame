import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
INITIAL_SPEED = 5  # 添加初始速度常量（原速度的50%）
SPEED_BOOST = 0.05  # 每次加速5%

# 初始化屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇")
clock = pygame.time.Clock()

# 蛇的初始设置
snake = [(WIDTH//2, HEIGHT//2)]
snake_direction = (0, 0)
food = (random.randint(0, (WIDTH-GRID_SIZE)//GRID_SIZE)*GRID_SIZE,
        random.randint(0, (HEIGHT-GRID_SIZE)//GRID_SIZE)*GRID_SIZE)
score = 0

# 在常量区新增
# 在常量区新增
import re  # 添加正则模块

GAME_TITLE = "贪吃蛇大作战"
SCORE_FILE = r"c:\Users\24559\Saved Games\snake_scores.csv"
BUTTON_COLOR = (100, 200, 100)

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

def generate_food():
    while True:
        new_food = (random.randint(0, (WIDTH-GRID_SIZE)//GRID_SIZE)*GRID_SIZE,
                    random.randint(0, (HEIGHT-GRID_SIZE)//GRID_SIZE)*GRID_SIZE)
        if new_food not in snake:
            return new_food

# 游戏主循环
running = True
game_over = False
current_speed = INITIAL_SPEED  # 添加速度变量
# 删除这个全局的游戏主循环（约从第95行开始）
# while running:
#     screen.fill(BLACK)
#     
#     处理事件
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if not game_over:
#                 if event.key == pygame.K_UP and snake_direction != (0, GRID_SIZE):
#                     snake_direction = (0, -GRID_SIZE)
#                 elif event.key == pygame.K_DOWN and snake_direction != (0, -GRID_SIZE):
#                     snake_direction = (0, GRID_SIZE)
#                 elif event.key == pygame.K_LEFT and snake_direction != (GRID_SIZE, 0):
#                     snake_direction = (-GRID_SIZE, 0)
#                 elif event.key == pygame.K_RIGHT and snake_direction != (-GRID_SIZE, 0):
#                     snake_direction = (GRID_SIZE, 0)
#             else:
#                 if event.key == pygame.K_r:
#                     snake = [(WIDTH//2, HEIGHT//2)]
#                     snake_direction = (0, 0)
#                     score = 0
#                     food = generate_food()
#                     game_over = False

#     if not game_over:
#         # 移动蛇
#         new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
#         snake.insert(0, new_head)
#         
#         # 吃食物检测
#         if snake[0] == food:
#             score += 10
#             food = generate_food()
#             current_speed = int(current_speed * (1 + SPEED_BOOST))  # 速度提升
#         else:
#             snake.pop()
#         
#         # 碰撞检测
#         if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
#             snake[0][1] < 0 or snake[0][1] >= HEIGHT or
#             snake[0] in snake[1:]):
#             game_over = True

#     # 绘制元素
#     draw_snake()
#     pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))
#     
#     # 显示分数
#     font = pygame.font.SysFont(None, 36)
#     text = font.render(f"Score: {score}", True, WHITE)
#     screen.blit(text, (10, 10))
#     
#     # 双选项处理逻辑
#     if game_over:
#         text = font.render("Game Over! Press R to restart", True, WHITE)
#         screen.blit(text, (WIDTH//2-150, HEIGHT//2))
#         options = font.render("R-重玩  ENTER-返回菜单", True, WHITE)
#         screen.blit(options, (WIDTH//2-180, HEIGHT//2+40))
#         
#         # 处理按键事件
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_r:
#                     # 重置游戏状态
#                     snake = [(WIDTH//2, HEIGHT//2)]
#                     snake_direction = (0, 0)
#                     score = 0
#                     food = generate_food()
#                     game_over = False
#                     current_speed = INITIAL_SPEED
#                 elif event.key == pygame.K_RETURN:
#                     # 返回主菜单时需要退出当前游戏循环
#                     running = False  # 改为退出循环而不是return

#         text = font.render("Game Over! Press R to restart", True, WHITE)
#         screen.blit(text, (WIDTH//2-150, HEIGHT//2))
#     
#     pygame.display.update()
#     clock.tick(current_speed)  # 修改帧率控制

# 新增文本输入框类
# 修正后的InputBox类（添加__init__方法）
class InputBox:
    def __init__(self, x, y, w, h, text=''):  # 添加构造函数参数
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = text
        self.font = pygame.font.SysFont(None, 36)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = True

    # 保持现有方法不变
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.color)
        return False

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    # 添加验证方法
    def validate(self):
        pattern = r'^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9\s（）]*$'
        if len(self.text.strip()) == 0:
            return False, "昵称不能为空！"
        if not re.match(pattern, self.text):
            return False, "首字符需为字母/中文，后续可包含数字、空格和中文括号"
        return True, ""

# 新增数据记录函数
def save_score(username, score):
    with open(SCORE_FILE, 'a') as f:
        timestamp = pygame.time.get_ticks() // 1000
        f.write(f"{username},{score},{timestamp}\n")

def get_high_scores():
    try:
        with open(SCORE_FILE, 'r') as f:
            scores = [line.strip().split(',') for line in f.readlines()]
            scores.sort(key=lambda x: -int(x[1]))
            return scores[:10]  # 返回前10名
    except FileNotFoundError:
        return []

# Add this new function below get_high_scores
def show_high_scores():
    scores = get_high_scores()
    back = False
    while not back:
        screen.fill(BLACK)
        font = pygame.font.SysFont('simhei', 36)
        title = font.render("高分榜单", True, GREEN)
        screen.blit(title, (WIDTH//2-80, 50))
        
        # Display scores
        y = 150
        if not scores:
            text = font.render("暂无记录", True, WHITE)
            screen.blit(text, (WIDTH//2-80, y))
        else:
            for i, (name, score, timestamp) in enumerate(scores[:10]):
                entry = font.render(f"{i+1}. {name}: {score}分", True, WHITE)
                screen.blit(entry, (100, y + i*40))
        
        # Display return instruction
        text = font.render("按ESC返回主菜单", True, WHITE)
        screen.blit(text, (WIDTH//2-140, HEIGHT-100))
        
        pygame.display.update()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                back = True
        
        clock.tick(30)

def start_screen():
    input_box = InputBox(WIDTH//2-100, HEIGHT//2-25, 200, 50)
    done = False
    while not done:
        screen.fill(BLACK)
        font = pygame.font.SysFont('simhei', 36)
        title = font.render("请输入玩家昵称：", True, WHITE)
        screen.blit(title, (WIDTH//2-120, HEIGHT//3))
        
        for event in pygame.event.get():
            if input_box.handle_event(event):
                valid, msg = input_box.validate()
                if valid:
                    return input_box.text.strip()
                else:
                    error_font = pygame.font.SysFont('simhei', 24)
                    error_text = error_font.render(msg, True, RED)
                    screen.blit(error_text, (WIDTH//2-150, HEIGHT//2+50))
        
        input_box.draw(screen)
        pygame.display.update()
        clock.tick(30)

class MainMenu:
    def __init__(self):
        self.selected = 0
        self.options = ["开始游戏", "高分榜单", "游戏说明", "游戏难度", "退出游戏"]
        # 新增菜单项矩形区域
        self.option_rects = [
            pygame.Rect(WIDTH//2-100, 150 + i*60, 200, 50) for i in range(5)
        ]

    def draw(self):
        screen.fill(BLACK)
        font = pygame.font.SysFont('simhei', 48)
        title = font.render(GAME_TITLE, True, GREEN)
        screen.blit(title, (WIDTH//2-120, 50))
        
        # 绘制带背景的菜单项
        item_font = pygame.font.SysFont('simhei', 36)
        for i, (text, rect) in enumerate(zip(self.options, self.option_rects)):
            color = GREEN if i == self.selected else WHITE
            # 添加按钮背景
            pygame.draw.rect(screen, BUTTON_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else (50,50,50), rect)
            text_surf = item_font.render(text, True, color)
            screen.blit(text_surf, (rect.x + 20, rect.y + 10))
        
        pygame.display.update()

# Remove duplicate set_difficulty function and keep this version
def set_difficulty(current):
    diff_menu = DifficultyMenu()
    while True:
        diff_menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return current
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    return {
                        pygame.K_1: (5, 0.03),
                        pygame.K_2: (8, 0.05),
                        pygame.K_3: (12, 0.08)
                    }[event.key]

# Fix main_game function structure
def main_game(username):
    # 添加全局变量声明
    global game_over, score, snake, snake_direction, food, current_speed
    
    # 初始化游戏状态（在函数开头添加）
    snake = [(WIDTH//2, HEIGHT//2)]
    snake_direction = (0, 0)
    food = generate_food()
    score = 0
    game_over = False
    current_speed = INITIAL_SPEED  # 使用全局难度设置

    # 重构游戏循环
    running = True
    while running:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 36)
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, GRID_SIZE):
                    snake_direction = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -GRID_SIZE):
                    snake_direction = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and snake_direction != (GRID_SIZE, 0):
                    snake_direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-GRID_SIZE, 0):
                    snake_direction = (GRID_SIZE, 0)
                elif event.key == pygame.K_r:  # 重置游戏
                    snake = [(WIDTH//2, HEIGHT//2)]
                    snake_direction = (0, 0)
                    score = 0
                    food = generate_food()
                    game_over = False

        # 游戏逻辑更新（移动到循环内部）
        if not game_over:
            # 移动蛇
            new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
            snake.insert(0, new_head)
            
            # 吃食物检测
            if snake[0] == food:
                score += 10
                food = generate_food()
                current_speed = int(current_speed * (1 + SPEED_BOOST))
            else:
                snake.pop()
            
            # 碰撞检测
            if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
                snake[0][1] < 0 or snake[0][1] >= HEIGHT or
                snake[0] in snake[1:]):
                game_over = True

        # 绘制游戏元素
        draw_snake()
        pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))
        
        # 游戏结束处理
        # 修改游戏结束处理逻辑
        if game_over:
            save_score(username, score)
            # 绘制结束界面
            game_over_font = pygame.font.SysFont(None, 36)
            text = game_over_font.render("Game Over! Press R to restart", True, WHITE)
            screen.blit(text, (WIDTH//2-150, HEIGHT//2))
            options = game_over_font.render("R-重玩  ENTER-返回菜单", True, WHITE)
            screen.blit(options, (WIDTH//2-180, HEIGHT//2+40))
            pygame.display.update()
            
            # 简化游戏结束事件处理
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 重玩
                        main_game(username)
                        return
                    elif event.key == pygame.K_RETURN:  # 返回主菜单
                        running = False
                        return

        pygame.display.update()
        clock.tick(current_speed)

# 新增难度设置函数
# 删除旧版无参数函数，保留新版带参数函数
def set_difficulty(current):  # 保留这个版本
    diff_menu = DifficultyMenu()
    while True:
        diff_menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    global INITIAL_SPEED, SPEED_BOOST
                    if event.key == pygame.K_1:  # 简单模式
                        INITIAL_SPEED = 5
                        SPEED_BOOST = 0.03
                    elif event.key == pygame.K_2:  # 普通模式
                        INITIAL_SPEED = 8
                        SPEED_BOOST = 0.05  
                    elif event.key == pygame.K_3:  # 困难模式
                        INITIAL_SPEED = 12
                        SPEED_BOOST = 0.08
                    return

# 新增难度菜单类
class DifficultyMenu:
    def __init__(self):
        self.options = [
            "1. 简单模式（慢速）",
            "2. 普通模式（中速）",
            "3. 困难模式（快速）"
        ]
    
    def draw(self):
        screen.fill(BLACK)
        font = pygame.font.SysFont('simhei', 36)
        title = font.render("请选择游戏难度：", True, GREEN)
        screen.blit(title, (WIDTH//2-150, 100))
        
        for i, text in enumerate(self.options):
            text_surf = font.render(text, True, WHITE)
            screen.blit(text_surf, (WIDTH//2-150, 200+i*60))
        
        pygame.display.update()

# 完善show_instruction函数
def show_instruction():
    instruction = [
        "使用方向键控制蛇的移动",
        "吃到红色食物增长身体并加速",
        "碰撞墙壁或自身会结束游戏",
        "按ESC键返回主菜单",
        "游戏难度影响初始速度和加速比例",
        "当前难度设置：",
        f"初始速度: {INITIAL_SPEED} 加速比率: {SPEED_BOOST*100}%"
    ]
    back = False
    while not back:
        screen.fill(BLACK)
        font = pygame.font.SysFont('simhei', 32)
        # 绘制说明文字
        for i, line in enumerate(instruction):
            text = font.render(line, True, WHITE)
            screen.blit(text, (100, 100 + i*40))
        # 处理返回事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                back = True
        pygame.display.update()
        clock.tick(30)

class PauseMenu:
    def __init__(self):
        self.selected = 0
        self.options = ["继续游戏", "退出游戏"]
    
    def draw(self):
        # 绘制半透明背景
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        # 绘制菜单项
        font = pygame.font.SysFont('simhei', 48)
        for i, text in enumerate(self.options):
            color = GREEN if i == self.selected else WHITE
            text_surf = font.render(text, True, color)
            screen.blit(text_surf, (WIDTH//2-100, HEIGHT//2-30 + i*60))
        pygame.display.update()
        
        # 绘制菜单项
        font = pygame.font.SysFont('simhei', 48)
        for i, text in enumerate(self.options):
            color = GREEN if i == self.selected else WHITE
            text_surf = font.render(text, True, color)
            screen.blit(text_surf, (WIDTH//2-100, HEIGHT//2-30 + i*60))
        pygame.display.update()

# 保留并确保主入口代码正确
if __name__ == "__main__":
    pygame.init()
    DEFAULT_DIFFICULTY = (8, 0.05)
    current_diff = DEFAULT_DIFFICULTY
    
    while True:  # 主菜单循环
        menu = MainMenu()
        menu_running = True
        
        while menu_running:
            menu.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 修改为鼠标控制
                elif event.type == pygame.MOUSEMOTION:
                    # 高亮悬停的选项
                    pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(menu.option_rects):
                        if rect.collidepoint(pos):
                            menu.selected = i
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(menu.option_rects):
                        if rect.collidepoint(pos):
                            if i == 0:  # 开始游戏
                                username = start_screen()
                                INITIAL_SPEED, SPEED_BOOST = current_diff
                                main_game(username)
                                menu_running = False
                            elif i == 1:  # 高分榜单
                                show_high_scores()
                            elif i == 2:  # 游戏说明
                                show_instruction()
                            elif i == 3:  # 难度设置
                                current_diff = set_difficulty(current_diff)
                            elif i == 4:  # 退出
                                pygame.quit()
                                sys.exit()
            clock.tick(15)