import cv2
import numpy as np


def left_power(img, lower=np.array([123, 88, 104]), upper=np.array([255, 178, 159])):
    power_left = 0
    try:
        img = img[417:, 0:290]
        mask = cv2.inRange(img, lower, upper)
        masked = cv2.bitwise_and(img, img, mask=mask)
        gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        gray[gray >= 100] = 255
        gray[gray < 100] = 0
        positions = np.argwhere(gray != 0)
        # print(np.amax(positions, axis=0)[1], " ", np.amin(positions, axis=0)[1])
        power_left = np.amax(positions, axis=0)[1] - np.amin(positions, axis=0)[1]
        # print("power left = ", power_left)
        # cv2.imshow('left',gray)
    except Exception:
        pass
    finally:
        return power_left > 190


def right_power(img, lower=np.array([123, 88, 104]), upper=np.array([255, 178, 159])):
    power_right = 0
    try:
        img = img[417:, 580:]
        mask = cv2.inRange(img, lower, upper)
        masked = cv2.bitwise_and(img, img, mask=mask)
        gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        gray[gray >= 100] = 255
        gray[gray < 100] = 0
        positions = np.argwhere(gray != 0)
        # print(np.amax(positions, axis=0)[1], " ", np.amin(positions, axis=0)[1])
        power_right = np.amax(positions, axis=0)[1] - np.amin(positions, axis=0)[1]
        # print("power right = ", power_right)
        # cv2.imshow('right', gray)
    except Exception:
        pass
    finally:
        return power_right > 190
