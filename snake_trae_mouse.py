#!/usr/bin/env python3
"""
贪吃蛇大作战 — 经典贪吃蛇游戏，支持鼠标操作、难度选择、高分榜单。

控制:
  方向键 — 控制蛇移动
  R — 游戏结束后重新开始
  Enter — 返回主菜单
  ESC — 返回上级菜单
  鼠标 — 菜单选择

依赖: pip install pygame
"""

import os
import re
import sys
import random
import pygame
from typing import Tuple, List, Optional

# ── 游戏常量 ──────────────────────────────────────────────

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20

# 颜色
WHITE  = (255, 255, 255)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
BLACK  = (0, 0, 0)
GRAY   = (50, 50, 50)
BUTTON_COLOR = (100, 200, 100)

GAME_TITLE = "贪吃蛇大作战"

# 难度预设: (初始速度, 每次加速比例)
DIFFICULTY_PRESETS = {
    "easy":   (5,  0.03),
    "normal": (8,  0.05),
    "hard":   (12, 0.08),
}

# ── 全局游戏状态 ──────────────────────────────────────────
# (保留为模块级以便各函数访问, 后续可重构为 GameState 类)

INITIAL_SPEED = DIFFICULTY_PRESETS["normal"][0]
SPEED_BOOST   = DIFFICULTY_PRESETS["normal"][1]

# 成绩文件路径（便携化 — 放在用户目录下）
SCORE_FILE = os.path.join(os.path.expanduser("~"), ".snake_scores.csv")


# ── 工具函数 ──────────────────────────────────────────────

def generate_food(snake: List[Tuple[int, int]]) -> Tuple[int, int]:
    """在空白位置生成食物"""
    while True:
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        if (x, y) not in snake:
            return (x, y)


def draw_snake(screen: pygame.Surface, snake: List[Tuple[int, int]]):
    """绘制蛇身"""
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x, y, GRID_SIZE, GRID_SIZE))


def save_score(username: str, score: int):
    """保存成绩到 CSV 文件"""
    os.makedirs(os.path.dirname(SCORE_FILE) or ".", exist_ok=True)
    with open(SCORE_FILE, 'a', encoding='utf-8') as f:
        timestamp = pygame.time.get_ticks() // 1000
        f.write(f"{username},{score},{timestamp}\n")


def get_high_scores() -> List[List[str]]:
    """读取高分榜单（前10名）"""
    try:
        with open(SCORE_FILE, 'r', encoding='utf-8') as f:
            scores = [line.strip().split(',') for line in f.readlines() if line.strip()]
            scores.sort(key=lambda x: -int(x[1]))
            return scores[:10]
    except (FileNotFoundError, ValueError):
        return []


# ── UI 组件 ───────────────────────────────────────────────

class InputBox:
    """文本输入框 — 用于输入玩家昵称"""

    def __init__(self, x: int, y: int, w: int, h: int, text: str = ''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = text
        self.font = pygame.font.SysFont('simhei', 36)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.color)
        return False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def validate(self) -> Tuple[bool, str]:
        """验证昵称合法性"""
        pattern = r'^[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9\s（）]*$'
        if len(self.text.strip()) == 0:
            return False, "昵称不能为空！"
        if not re.match(pattern, self.text):
            return False, "首字符需为字母/中文，后续可包含数字、空格和中文括号"
        return True, ""


class MainMenu:
    """主菜单"""

    def __init__(self):
        self.selected = 0
        self.options = ["开始游戏", "高分榜单", "游戏说明", "游戏难度", "退出游戏"]
        self.option_rects = [
            pygame.Rect(WIDTH // 2 - 100, 150 + i * 60, 200, 50)
            for i in range(5)
        ]

    def draw(self, screen: pygame.Surface):
        screen.fill(BLACK)
        font_title = pygame.font.SysFont('simhei', 48)
        font_item  = pygame.font.SysFont('simhei', 36)

        title = font_title.render(GAME_TITLE, True, GREEN)
        screen.blit(title, (WIDTH // 2 - 120, 50))

        mouse_pos = pygame.mouse.get_pos()
        for i, (text, rect) in enumerate(zip(self.options, self.option_rects)):
            hover = rect.collidepoint(mouse_pos)
            bg_color = BUTTON_COLOR if hover else GRAY
            text_color = GREEN if (i == self.selected or hover) else WHITE

            pygame.draw.rect(screen, bg_color, rect)
            text_surf = font_item.render(text, True, text_color)
            screen.blit(text_surf, (rect.x + 20, rect.y + 10))

        pygame.display.update()


class DifficultyMenu:
    """难度选择菜单"""

    def __init__(self):
        self.options = [
            "1. 简单模式（慢速）",
            "2. 普通模式（中速）",
            "3. 困难模式（快速）",
        ]

    def draw(self, screen: pygame.Surface):
        screen.fill(BLACK)
        font = pygame.font.SysFont('simhei', 36)
        title = font.render("请选择游戏难度：", True, GREEN)
        screen.blit(title, (WIDTH // 2 - 150, 100))

        for i, text in enumerate(self.options):
            text_surf = font.render(text, True, WHITE)
            screen.blit(text_surf, (WIDTH // 2 - 150, 200 + i * 60))

        pygame.display.update()


class PauseMenu:
    """暂停菜单"""

    def __init__(self):
        self.selected = 0
        self.options = ["继续游戏", "退出游戏"]

    def draw(self, screen: pygame.Surface):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont('simhei', 48)
        for i, text in enumerate(self.options):
            color = GREEN if i == self.selected else WHITE
            text_surf = font.render(text, True, color)
            screen.blit(text_surf, (WIDTH // 2 - 100, HEIGHT // 2 - 30 + i * 60))

        pygame.display.update()


# ── 界面函数 ──────────────────────────────────────────────

def start_screen() -> str:
    """显示开始画面，让玩家输入昵称"""
    input_box = InputBox(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    clock = pygame.time.Clock()
    error_msg = ""

    while True:
        screen = pygame.display.get_surface()
        screen.fill(BLACK)
        font = pygame.font.SysFont('simhei', 36)
        title = font.render("请输入玩家昵称：", True, WHITE)
        screen.blit(title, (WIDTH // 2 - 120, HEIGHT // 3))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if input_box.handle_event(event):
                valid, msg = input_box.validate()
                if valid:
                    return input_box.text.strip()
                else:
                    error_msg = msg

        input_box.draw(screen)

        if error_msg:
            error_font = pygame.font.SysFont('simhei', 24)
            error_text = error_font.render(error_msg, True, RED)
            screen.blit(error_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))

        pygame.display.update()
        clock.tick(30)


def show_high_scores():
    """显示高分榜单"""
    scores = get_high_scores()
    clock = pygame.time.Clock()
    screen = pygame.display.get_surface()

    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont('simhei', 36)
        title = font.render("高分榜单", True, GREEN)
        screen.blit(title, (WIDTH // 2 - 80, 50))

        y = 150
        if not scores:
            text = font.render("暂无记录", True, WHITE)
            screen.blit(text, (WIDTH // 2 - 80, y))
        else:
            for i, (name, sc, _) in enumerate(scores[:10]):
                entry = font.render(f"{i + 1}. {name}: {sc}分", True, WHITE)
                screen.blit(entry, (100, y + i * 40))

        text = font.render("按ESC返回主菜单", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 140, HEIGHT - 100))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        clock.tick(30)


def show_instruction():
    """显示游戏说明"""
    global INITIAL_SPEED, SPEED_BOOST
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    instructions = [
        "使用方向键控制蛇的移动",
        "吃到红色食物增长身体并加速",
        "碰撞墙壁或自身会结束游戏",
        "R — 重玩 | Enter — 返回菜单 | ESC — 返回上级",
        "游戏难度影响初始速度和加速比例",
        "",
        f"当前难度: 初始速度={INITIAL_SPEED}  加速比率={SPEED_BOOST*100:.0f}%",
    ]

    while True:
        screen.fill(BLACK)
        font = pygame.font.SysFont('simhei', 32)
        for i, line in enumerate(instructions):
            text = font.render(line, True, WHITE)
            screen.blit(text, (100, 100 + i * 40))

        text = font.render("按ESC返回主菜单", True, GREEN)
        screen.blit(text, (100, 100 + len(instructions) * 40 + 20))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        clock.tick(30)


def set_difficulty():
    """难度选择界面 — 返回 (INITIAL_SPEED, SPEED_BOOST)"""
    global INITIAL_SPEED, SPEED_BOOST
    screen = pygame.display.get_surface()
    diff_menu = DifficultyMenu()
    clock = pygame.time.Clock()

    while True:
        diff_menu.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return (INITIAL_SPEED, SPEED_BOOST)
                elif event.key == pygame.K_1:
                    INITIAL_SPEED, SPEED_BOOST = DIFFICULTY_PRESETS["easy"]
                    return DIFFICULTY_PRESETS["easy"]
                elif event.key == pygame.K_2:
                    INITIAL_SPEED, SPEED_BOOST = DIFFICULTY_PRESETS["normal"]
                    return DIFFICULTY_PRESETS["normal"]
                elif event.key == pygame.K_3:
                    INITIAL_SPEED, SPEED_BOOST = DIFFICULTY_PRESETS["hard"]
                    return DIFFICULTY_PRESETS["hard"]
        clock.tick(30)


# ── 核心游戏逻辑 ──────────────────────────────────────────

def main_game(username: str):
    """主游戏循环"""
    snake = [(WIDTH // 2, HEIGHT // 2)]
    snake_direction = (0, 0)
    food = generate_food(snake)
    score = 0
    game_over = False
    current_speed = INITIAL_SPEED

    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 36)

        # 事件处理
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
                elif event.key == pygame.K_r and game_over:
                    # 重新开始
                    snake = [(WIDTH // 2, HEIGHT // 2)]
                    snake_direction = (0, 0)
                    food = generate_food(snake)
                    score = 0
                    game_over = False
                    current_speed = INITIAL_SPEED

        # 游戏逻辑
        if not game_over:
            new_head = (snake[0][0] + snake_direction[0],
                        snake[0][1] + snake_direction[1])
            snake.insert(0, new_head)

            if snake[0] == food:
                score += 10
                food = generate_food(snake)
                current_speed = int(current_speed * (1 + SPEED_BOOST))
            else:
                snake.pop()

            # 碰撞检测
            if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
                snake[0][1] < 0 or snake[0][1] >= HEIGHT or
                snake[0] in snake[1:]):
                game_over = True

        # 绘制
        draw_snake(screen, snake)
        pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # 游戏结束处理
        if game_over:
            save_score(username, score)
            go_font = pygame.font.SysFont(None, 36)
            text = go_font.render("Game Over! Press R to restart", True, WHITE)
            screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2))
            options = go_font.render("R-重玩  ENTER-返回菜单", True, WHITE)
            screen.blit(options, (WIDTH // 2 - 180, HEIGHT // 2 + 40))
            pygame.display.update()

            # 等待玩家选择
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main_game(username)
                        return
                    elif event.key == pygame.K_RETURN:
                        return

        pygame.display.update()
        clock.tick(current_speed)


# ── 主入口 ────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    current_diff = DIFFICULTY_PRESETS["normal"]

    while True:
        menu = MainMenu()
        in_menu = True

        while in_menu:
            menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(menu.option_rects):
                        if rect.collidepoint(pos):
                            menu.selected = i
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(menu.option_rects):
                        if rect.collidepoint(pos):
                            if i == 0:   # 开始游戏
                                username = start_screen()
                                global INITIAL_SPEED, SPEED_BOOST
                                INITIAL_SPEED, SPEED_BOOST = current_diff
                                main_game(username)
                                in_menu = False
                            elif i == 1:  # 高分榜单
                                show_high_scores()
                            elif i == 2:  # 游戏说明
                                show_instruction()
                            elif i == 3:  # 难度设置
                                current_diff = set_difficulty()
                            elif i == 4:  # 退出
                                pygame.quit()
                                sys.exit()
            clock.tick(15)


if __name__ == "__main__":
    main()
