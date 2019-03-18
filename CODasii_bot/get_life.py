import cv2
import numpy as np


def get_left_hero_life(img, lower = np.array([45, 0, 45]), upper = np.array([244, 255, 255])):
    life_left = -1
    try:
        img = img[0:18]
        img = img[:, 0:390]
        mask = cv2.inRange(img, lower, upper)
        masked = cv2.bitwise_and(img, img, mask=mask)
        gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        gray[gray>=100] = 255
        gray[gray<100] = 0
        positions = np.argwhere(gray != 0)
        life_left = np.amax(positions, axis=0)[1] - np.amin(positions, axis=0)[1]
    except Exception:
        pass
    finally:
        return life_left


def get_right_hero_life(img, lower= np.array([45, 0, 45]), upper= np.array([244, 255, 255])):
    life_right = -1
    try:
        img = img[0:18]
        img = img[:, 430:]
        mask = cv2.inRange(img, lower, upper)
        masked = cv2.bitwise_and(img, img, mask=mask)
        gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        gray[gray >= 100] = 255
        gray[gray < 100] = 0
        positions = np.argwhere(gray != 0)
        # print(np.amax(positions, axis=0)[1], " ", np.amin(positions, axis=0)[1])
        life_right = np.amax(positions, axis=0)[1] - np.amin(positions, axis=0)[1]
    except Exception:
        pass
    finally:
        return life_right
