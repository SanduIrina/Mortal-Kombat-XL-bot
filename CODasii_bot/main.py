import cv2, sys
import numpy as np
from random import randint

from client import startListening

from commands import Player, actions
from get_life import get_left_hero_life, get_right_hero_life
from get_power_bar import left_power, right_power
from combos import SubzeroCombos, ScorpionCombos

p = Player(p1_key='ao73y4nitd4jsuoh', p2_key='ly41qematdd5lcx0', admin_key='2a6xoougvdd0fpoe')
SUBZERO = 1
SCORPIO = 2

SUBZERO_1 = 5
SUBZERO_2 = 6

LEFT = 3
RIGHT = 4

lower_scorpio = np.array([125, 48, 33])
upper_scorpio = np.array([255, 255, 86])

lower_subzero = np.array([33, 74, 92])
upper_subzero = np.array([54, 255, 255])

lower_finish = np.array([138, 0, 0])
upper_finish = np.array([255, 53, 255])

lower1 = np.array([23, 55, 97])
upper1 = np.array([47, 66, 119])

lower2 = np.array([25, 93, 107])
upper2 = np.array([58, 112, 125])


def get_bounding_box(img, out_img, lower, upper, color):
    mask = cv2.inRange(img, lower, upper)
    masked = cv2.bitwise_and(img, img, mask=mask)
    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    positions = np.argwhere(gray > 40)
    # print positions[(len(positions) - 50): ]
    # if len(positions) > 10:
    #     positions = positions[10:]
    avg = np.median(positions, axis=0)

    fx = avg[1]
    fy = avg[0]

    # cv2.rectangle(out_img, (int(fx), int(fy)), (int(fx) + 1, int(fy) + 1), color, 3)
    # cv2.rectangle(masked, (int(fx), int(fy)), (int(fx) + 1, int(fy) + 1), color, 3)

    return avg, masked


def subzero_decide(my_side, hp_diff, d, fatality, power):
    back = actions.LEFT if my_side == LEFT else actions.RIGHT
    forward = actions.RIGHT if my_side == LEFT else actions.LEFT

    if fatality and not p.did_fatal:
        p.did_fatal = True
        print "fatality ", p.cmd_q.qsize()
        while not p.cmd_q.empty():
            try:
                p.cmd_q.get_nowait()
            except Exception:
                pass
        print "fatality ", p.cmd_q.qsize()
        # if d < 0.1:
        #     print "snd combo"
        p.send_combo(SubzeroCombos.kold_fatal(back, forward))
        p.send_combo(SubzeroCombos.kold_fatal(back, forward))
        p.send_combo(SubzeroCombos.kold_fatal(back, forward))
        p.send_combo(SubzeroCombos.kold_fatal(back, forward))
        return
        # else:
        #     print "get closer %d" % d
        #     p.move_command(forward, timeout=d)

    # if power:
    #     p.send_combo([actions.LEFT, actions.RIGHT], p2=(p.my_p == 'p2'))
    #     return

    if d < 0.1:
        if hp_diff < -60:
            p.send_combo(SubzeroCombos.sword(), anim_timeout=0.06)
        elif hp_diff < -30:
            p.send_combo(SubzeroCombos.iceBurst(back), anim_timeout=0.06)

        if randint(0, 100) <= 30:
            p.send_simple_hits(timeout=0.05)
        else:
            p.send_combo(SubzeroCombos.sword(), anim_timeout=0.06)
    elif d < 0.2:
        p.send_combo(SubzeroCombos.slash(forward), anim_timeout=0.06)
    elif d < 0.3:
        p.send_combo(SubzeroCombos.hammer(back), anim_timeout=0.09)
    # elif d < 0.4:
    elif d < 0.5:
        p.send_combo(SubzeroCombos.slide(back, forward), anim_timeout=0.1)
    else:
        # p.move_command(actions.LEFT, p.my_p == 'p2')
        if randint(0, 100) <= 60:
            p.send_combo(SubzeroCombos.iceBall(forward), anim_timeout=0.1)
        else:
            p.move_command(forward, timeout=1)


def scorpio_decide(my_side, hp_diff, d, subzero_p, scorpio_p, fatality, power):
    back = actions.LEFT if my_side == LEFT else actions.RIGHT
    forward = actions.RIGHT if my_side == LEFT else actions.LEFT

    # if hp_diff > -20:
    if d < 0.1:
        p.send_combo(ScorpionCombos.teleport(back))
    else:
        p.send_combo(ScorpionCombos.spear(back, forward), anim_timeout=0.1)
    # else:
    # if d < 0.1:
    #     p.send_combo(ScorpionCombos.teleport(back))
    # else:
    #     p.send_combo(ScorpionCombos.spear(back, forward))


def dist(p1, p2):
    d = p1 - p2
    return d[0] ** 2 + d[1] ** 2


def make_decision(subzero_p, scorpio_p, p1_hp, p2_hp, fatality, power):
    d = subzero_p - scorpio_p
    d = d[0] ** 2 + d[1] ** 2
    hp_diff = p1_hp - p2_hp
    if p.my_p == 'p2':
        hp_diff *= -1

    if p.my_hero == SUBZERO:
        if subzero_p[1] < scorpio_p[1]:
            my_side = LEFT
        else:
            my_side = RIGHT
    else:
        if subzero_p[1] < scorpio_p[1]:
            my_side = RIGHT
        else:
            my_side = LEFT

    # print d, hp_diff
    if p.my_hero == SUBZERO:
        subzero_decide(my_side, hp_diff, d, fatality, power)
        return
    else:
        scorpio_decide(my_side, hp_diff, d, subzero_p, scorpio_p, fatality, power)


def get_no_color(frame, lower, upper):
    mask = cv2.inRange(frame, lower, upper)
    n = cv2.countNonZero(mask)
    return n


def get_half_box(orig_frame, frame, lower, upper, left_side, color):
    if left_side:
        half_frame = orig_frame[:, :400]
    else:
        half_frame = orig_frame[:, 400:]
    mask = cv2.inRange(half_frame, lower, upper)
    masked = cv2.bitwise_and(half_frame, half_frame, mask=mask)
    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    positions = np.argwhere(gray > 40)
    # print positions[(len(positions) - 50): ]
    # if len(positions) > 10:
    #     positions = positions[10:]
    avg = np.median(positions, axis=0)
    if not left_side:
        avg[1] += 400

    fx = avg[1]
    fy = avg[0]

    # cv2.rectangle(frame, (int(fx), int(fy)), (int(fx) + 1, int(fy) + 1), color, 3)
    # cv2.rectangle(masked, (int(fx) - 400 if not left_side else 0, int(fy)), (int(fx) - 400 if not left_side else 0 + 1, int(fy) + 1), color, 3)

    return avg, masked


def example(frame):
    try:
        frame = frame[100:len(frame) - 50]
        orig_frame = np.copy(frame)

        mask = cv2.inRange(frame, lower_finish, upper_finish)
        fatality = cv2.countNonZero(mask) > 4000

        try:
            if not p.started_game:
                hp = get_left_hero_life(frame)
                if hp > 10:
                    print "hp: ", hp
                    p.started_game = True
                    sz_n = get_no_color(frame, lower_subzero, upper_subzero)
                    sc_n = get_no_color(frame, lower_scorpio, upper_scorpio)

                    if sz_n > 50:
                        p.subzero = True
                    if sc_n > 50:
                        p.scorpio = True
                if p.my_p is None:
                    p.my_p = p.get_status(False)['player']
                    if p.my_p == 'p2':
                        p.back_now = actions.RIGHT
                    else:
                        p.back_now = actions.LEFT
                    p.panic_attack = False
            else:
                if p.my_p == 'p2':
                    power = right_power(img=orig_frame)
                else:
                    power = left_power(img=orig_frame)

                if p.subzero is None:
                    # 2 scorpions
                    back = p.back_now
                    forward = actions.LEFT if back == actions.RIGHT else actions.RIGHT
                    p.move_command(back, timeout=0.5)
                    if p.panic_attack:
                        p.send_combo(ScorpionCombos.spear(back, forward))
                    else:
                        p.send_combo(ScorpionCombos.teleport(back), True)
                        p.back_now = actions.LEFT if p.back_now == actions.RIGHT else actions.RIGHT
                    p.panic_attack = not p.panic_attack
                elif p.scorpio is None:
                    # 2 subzeros
                    sz_p1, res_sz1 = get_bounding_box(orig_frame, frame, lower1, upper1, (0, 0, 255))
                    sz_p2, res_sz2 = get_bounding_box(orig_frame, frame, lower2, upper2, (0, 255, 0))

                    # cv2.imshow('sz1', res_sz1)
                    # cv2.imshow('sz2', res_sz2)
                    #
                    if p.my_hero is None:
                        if p.my_p == 'p1':
                            p.my_hero = SUBZERO_1
                            print "subzero 1"
                        else:
                            p.my_hero = SUBZERO_2
                            print "subzero 2"

                    left_hp = get_left_hero_life(orig_frame)
                    right_hp = get_right_hero_life(orig_frame)

                    # sz_sz(sz_p1, sz_p2, left_hp, right_hp, 0, 0)
                    hp_diff = left_hp - right_hp
                    if p.my_p == 'p2':
                        hp_diff *= -1

                    if p.my_hero == SUBZERO_1:
                        if sz_p1[1] < sz_p2[1]:
                            my_side = LEFT
                            # print "left"
                        else:
                            my_side = RIGHT
                            # print "right"
                    else:
                        if sz_p1[1] < sz_p2[1]:
                            my_side = RIGHT
                            # print "right"
                        else:
                            my_side = LEFT
                            # print "left"

                    sz_p1[0] /= frame.shape[0]
                    sz_p1[1] /= frame.shape[1]
                    sz_p2[0] /= frame.shape[0]
                    sz_p2[1] /= frame.shape[1]
                    d = dist(sz_p1[1], sz_p2[1])

                    subzero_decide(my_side, hp_diff, d, fatality, 0)

                    # back = p.back_now
                    # forward = actions.LEFT if back == actions.RIGHT else actions.RIGHT
                    # p.move_command(back, timeout=0.5)
                    # if p.panic_attack:
                    #     prob = randint(0, 200)
                    #     if prob <= 80:
                    #         p.send_combo(SubzeroCombos.sword(), anim_timeout=0.06)
                    #     elif prob <= 120:
                    #         p.send_combo(SubzeroCombos.hammer(back), anim_timeout=0.09)
                    #     elif prob <= 140:
                    #         p.send_combo(SubzeroCombos.slide(back, forward), anim_timeout=0.08)
                    #     elif prob <= 160:
                    #         p.send_combo(SubzeroCombos.iceBall(forward), anim_timeout=0.1)
                    #     elif prob <= 180:
                    #         p.send_simple_hits(timeout=0.05)
                    #     else:
                    #         p.send_combo(SubzeroCombos.slash(forward))
                    # else:
                    #     p.send_combo(SubzeroCombos.iceBurst(back))
                    # p.panic_attack = not p.panic_attack
                else:
                    sz_p, res_subzero = get_bounding_box(orig_frame, frame, lower_subzero, upper_subzero, (0, 0, 255))
                    sc_p, res_scorpio = get_bounding_box(orig_frame, frame, lower_scorpio, upper_scorpio, (0, 255, 0))
                    # cv2.imshow('subzero', res_subzero)
                    # cv2.imshow('scorpio', res_scorpio)

                    if p.my_hero is None:
                        if p.my_p == 'p1':
                            # im player 1, start left
                            if sz_p[1] < sc_p[1]:
                                # subzero is left
                                p.my_hero = SUBZERO
                                print "subzero p1"
                            else:
                                # scorpio is left
                                p.my_hero = SCORPIO
                                print "scorpio p1"
                        else:
                            # im player 2, start right
                            if sz_p[1] < sc_p[1]:
                                # scorpio is right
                                p.my_hero = SCORPIO
                                print "scorpio p2"
                            else:
                                # subzero is right
                                p.my_hero = SUBZERO
                                print "subzero p2"

                    if p.ready:
                        sz_p[0] /= frame.shape[0]
                        sz_p[1] /= frame.shape[1]
                        sc_p[0] /= frame.shape[0]
                        sc_p[1] /= frame.shape[1]

                        left_hp = get_left_hero_life(orig_frame)
                        right_hp = get_right_hero_life(orig_frame)
                        # print n, n > 4000
                        make_decision(sz_p, sc_p, left_hp, right_hp, fatality, power)
        except Exception as e:
            pass
            # print "exception: ", e

        cv2.imshow('client', frame)
        cv2.waitKey(1)

    except Exception:
        pass


UDP_IP = "0.0.0.0"
UDP_PORT = 10000
if (len(sys.argv) > 1):
    UDP_PORT = int(sys.argv[1])
startListening(UDP_IP, UDP_PORT, example)
