# test
import pygame
import json
import sys
import os

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def validate_nick(nick):
    if not isinstance(nick, str) or len(nick) > 25:
        return "Player"
    else:
        return nick

def oobe_validate_nick(nick):
    if len(nick) > 25:
        error_sound.play()
        return False
    else:
        return True

data = load_json("data.json")

RESET = {
    "first_launch": True,
    "nick": "",
    "skin": "",
    "background": "",
    "accent_color": "white",
    "lang": "en",
    "assets_dir": "assets"
}

pygame.init()

WIDTH = 640
HEIGHT = 480

menu_sound = pygame.mixer.Sound(os.path.join(data["assets_dir"], "sounds", "menu.mp3"))

last_menu_sound = 0

error_sound = pygame.mixer.Sound(os.path.join(data["assets_dir"], "sounds", "error.mp3"))

arial_bold = pygame.font.Font(os.path.join(data["assets_dir"], "fonts", "ariblk.ttf"), 50)
arial_bold_small = pygame.font.Font(os.path.join(data["assets_dir"], "fonts", "ariblk.ttf"), 15)

if data["first_launch"]:
    scene = "oobe"
    oobe_progress = "welcome"
    nick_input = ""
    cursor_x = 185
    cursor_x_add = 10
    cursor_x_minus = 10
    save_json("data.json", RESET)
else:
    data["nick"] = validate_nick(data["nick"])
    save_json("data.json", data)
    scene = "menu"

display = pygame.display.set_mode((WIDTH, HEIGHT))

can_click = True

if scene == "menu":
    menu_sound.play()

while True:
    display.fill(pygame.Color("blue"))
    mouse = pygame.mouse.get_pos()
    exit_oobe_button = pygame.image.load(os.path.join(data["assets_dir"], "images", "Oobe_exit_button.png")).convert_alpha()
    exit_oobe_button_rect = exit_oobe_button.get_rect(topleft=(0, 416))
    if scene == "oobe":
        if oobe_progress == "welcome":
            if data["lang"] == "en":
                welcome_text = arial_bold.render("Welcome!", True, pygame.Color(data["accent_color"]))
            if data["lang"] == "ru":
                welcome_text = arial_bold.render("Добро пожаловать!", True, pygame.Color(data["accent_color"]))
            if data["lang"] == "en":
                language_select = pygame.image.load(os.path.join(data["assets_dir"], "images", "English_oobe_select_button.png")).convert_alpha()
                language_select_rect = language_select.get_rect(topleft=(256, 208))
            if data["lang"] == "ru":
                language_select = pygame.image.load(os.path.join(data["assets_dir"], "images", "Russian_oobe_select_button.png")).convert_alpha()
                language_select_rect = language_select.get_rect(topleft=(256, 208))
            if data["lang"] == "en":
                display.blit(welcome_text, (200, 20))
            if data["lang"] == "ru":
                display.blit(welcome_text, (60, 20))
            next_button = pygame.image.load(os.path.join(data["assets_dir"], "images", "Next_button.png")).convert_alpha()
            next_button_rect = next_button.get_rect(topleft=(256, 320))
            display.blit(next_button, next_button_rect)
            display.blit(language_select, language_select_rect)
        if oobe_progress == "nick":
            if data["lang"] == "en":
                nick_enterbar = pygame.image.load(os.path.join(data["assets_dir"], "images", "English_oobe_nick_enterbar.png")).convert_alpha()
            if data["lang"] == "ru":
                nick_enterbar = pygame.image.load(os.path.join(data["assets_dir"], "images", "Russian_oobe_nick_enterbar.png")).convert_alpha()
            display.blit(nick_enterbar, (170, 215))
            display.blit(arial_bold_small.render(nick_input, False, pygame.Color("black")), (185, 242))
            pygame.draw.line(display, pygame.Color("black"), (cursor_x, 240), (cursor_x, 262), 2)
            next_button = pygame.image.load(os.path.join(data["assets_dir"], "images", "Next_button.png")).convert_alpha()
            next_button_rect = next_button.get_rect(topleft=(256, 320))
            display.blit(next_button, next_button_rect)
        if oobe_progress == "complete":
            pass
        display.blit(exit_oobe_button, exit_oobe_button_rect)
        if exit_oobe_button_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
    if scene == "menu":
        if pygame.time.get_ticks() - last_menu_sound > 17000:
            menu_sound.play()
            last_menu_sound = pygame.time.get_ticks()
    pygame.display.flip()
    for event in pygame.event.get():
        if scene == "oobe" and oobe_progress == "welcome" and event.type == pygame.MOUSEBUTTONDOWN and language_select_rect.collidepoint(mouse):
            if data["lang"] == "ru":
                data["lang"] = "en"
                save_json("data.json", data)
            else:
                data["lang"] = "ru"
                save_json("data.json", data)
        if scene == "oobe" and oobe_progress == "welcome" and event.type == pygame.MOUSEBUTTONDOWN and next_button_rect.collidepoint(mouse) and can_click:
            oobe_progress = "nick"
            can_click = False
        if scene == "oobe" and oobe_progress == "nick":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(nick_input) > 0:
                    nick_input = nick_input[:-1]
                    cursor_x -= cursor_x_minus
                elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT, pygame.K_LMETA, pygame.K_RMETA, pygame.K_MODE):
                    pass
                elif event.key == pygame.K_RETURN:
                    data["nick"] = nick_input
                    save_json("data.json", data)
                    oobe_progress = "complete"
                else:
                    if oobe_validate_nick(nick_input) and event.unicode.isprintable():
                        nick_input += event.unicode
                        cursor_x += cursor_x_add
            if scene == "oobe" and oobe_progress == "nick" and event.type == pygame.MOUSEBUTTONDOWN and next_button_rect.collidepoint(mouse) and can_click:
                oobe_progress = "complete"
                can_click = False
        if event.type == pygame.MOUSEBUTTONUP:
            can_click = True
        if event.type == pygame.QUIT:
            if data["first_launch"]:
                save_json("data.json", RESET)
            sys.exit()