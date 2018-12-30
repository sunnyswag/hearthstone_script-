import cv2 as cv
import numpy as np
import time
from PIL import ImageGrab
import pyautogui as pymouse


def mouse_drag_from_to(fromx, fromy, tox, toy):
    pymouse.moveTo(fromx, fromy)
    pymouse.dragTo(tox, toy, duration=0.3)


def mouse_click(inx, iny):
    pymouse.click(inx, iny)


def atack(fromx, fromy):
    mouse_click(fromx, fromy)
    pymouse.moveTo(960, 800, duration=0.3)
    enemy_sneer = detect_sneer()
    if len(enemy_sneer):  # 检测到嘲讽怪
        mouse_click(490 + enemy_sneer[0], 360)
        time.sleep(1)
    else:
        mouse_click(960, 210)
        time.sleep(1)


def cards_out():
    # 出牌
    mouse_drag_from_to(604, 1034, 960, 700)
    mouse_drag_from_to(700, 1034, 960, 700)
    mouse_drag_from_to(768, 1034, 960, 700)
    mouse_drag_from_to(950, 1034, 960, 700)
    mouse_drag_from_to(1056, 1034, 960, 700)
    mouse_drag_from_to(1172, 1034, 960, 700)

    # 英雄技能
    mouse_click(1130, 820)
    mouse_click(100,100)
    time.sleep(1)


def detect_and_return_probability(pix, x1, y1, x2, y2):
    time.sleep(1.3)
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))  # x1,y1,x2,y2
    img_np = np.array(img)

    im1 = cv.imread(pix)
    hist1 = cv.calcHist([im1], [0], None, [256], [0, 256])
    hist2 = cv.calcHist([img_np], [0], None, [256], [0, 256])

    return cv.compareHist(hist1, hist2, cv.HISTCMP_CORREL)


# 敌方嘲讽随从
def detect_sneer():
    img = ImageGrab.grab(bbox=(450, 300, 1470, 500))
    img_np = np.array(img)
    img_canny = cv.Canny(img_np, 600, 900)
    template = cv.imread("images/canny.png", 0)

    res = cv.matchTemplate(img_canny, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.3)
    return np.unique(loc[1])


# 我放随从
def in_range(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower_red = np.array([35, 43, 46])
    upper_red = np.array([77, 255, 255])
    mask = cv.inRange(hsv, lower_red, upper_red)
    return mask


def detect_my_attend():
    img = ImageGrab.grab(bbox=(450, 490, 1470, 690))
    img_np = np.array(img)
    img_in_range = in_range(img_np)
    template = cv.imread("images/range.png", 0)

    res = cv.matchTemplate(img_in_range, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.5)
    return np.unique(loc[1])


while True:
    # 游戏开始
    time.sleep(2)
    mouse_click(1407, 886)
    # # 确定开始手牌
    time.sleep(40)
    mouse_click(965, 860)
    time.sleep(10)
    # 进行游戏
    while True:
        mouse_click(100, 100)
        mouse_click(100, 100)
        # print(detect_and_return_probability("base/my_turn_yellow.png", 1460, 460, 1600, 530))
        if detect_and_return_probability("images/my_turn_yellow.png", 1460, 460, 1600, 530) > 0.3\
                or detect_and_return_probability("images/my_turn_yellow.png", 1460, 460, 1600, 530) < 0.04:
            cards_out()
            if 0.3 < detect_and_return_probability("images/my_turn_green.png", 1460, 460, 1600, 530) < 0.4:
                mouse_click(1530, 500)
                mouse_click(100, 100)
            else:
                while True:  # 检测到可以攻击
                    my_attended = detect_my_attend()
                    if len(my_attended):
                        atack(490 + my_attended[0], 550)
                    else:
                        break
                mouse_click(1530, 500)
                mouse_click(100, 100)
        elif 0.3 < detect_and_return_probability("images/my_turn_green.png", 1460, 460, 1600, 530) < 0.4:
            mouse_click(1530, 500)
            mouse_click(100, 100)

        elif detect_and_return_probability("images/enemy_turn.png", 1460, 460, 1600, 530) > 0.19:  # 对手回合
            time.sleep(5)

        if detect_and_return_probability("images/start_game.png", 1270, 790, 1490,
                                         990) > 0.9:  # 游戏结束多次点击后是否已经到了
            break
