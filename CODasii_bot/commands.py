from time import sleep

import socketio
import requests
from threading import Thread
from Queue import Queue


class actions:
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"
    FRONT_PUNCH = "front_punch"
    BACK_PUNCH = "back_punch"
    FRONT_KICK = "front_kick"
    BACK_KICK = "back_kick"
    INTERACT = "interact"
    THROW = "throw"
    BLOCK = "block"


class commands:
    ACTION_COMMAND = 'command'
    PLAYER_SELECT = 'player_select'
    STREAM_CONFIG = 'stream_config'
    ADMIN = 'admin'
    GET_STATUS = 'get_status'
    NEW_2P_GAME = 'new_2p_game'
    IN_GAME_TO_RESET_GAME = 'in_game_to_reset_game'


class champions:
    SCORPIO = "scorpio"
    SUBZERO = "subzero"


class menu_keys:
    UP = "up"
    DOWN = "down"
    LEFT = 'left'
    RIGHT ='right'
    ENTER ='enter'
    ESCAPE = 'escape'


class Player(Thread):
    url = 'http://10.81.176.97/'

    def __init__(self, p1_key, p2_key, admin_key, post_game_details=True):
        super(Player, self).__init__()
        self.p1_key = 'ao73y4nitd4jsuoh'
        self.p2_key = 'ao73y4nitd4jsuoh'
        self.admin_key = admin_key
        self.hide_post_game_details = post_game_details
        self.sio = socketio.Client()
        self.sio.connect('http://10.81.176.97')
        self.cmd_q = Queue()
        self.start()
        self.ready = True
        self.my_hero = None
        self.my_p = None
        self.scorpio = None
        self.subzero = None
        self.started_game = False
        self.panic_attack = False
        self.back_now = None
        self.did_fatal = False

    def get_status(self, p2):
        key = self.p2_key if p2 else self.p1_key
        body = {
            "key": key
        }
        r = requests.post(self.url + commands.GET_STATUS, json=body)
        print r.status_code
        return r.json()

    def __del__(self):
        self.sio.disconnect()

    def run(self):
        cmd = self.cmd_q.get()
        while cmd is not None:
            self.ready = False
            if cmd[0] == 'combo':
                for c in cmd[1]:
                    self.sio.emit('command', c)
                    sleep(0.05)
                sleep(0.05)
                for c in cmd[2]:
                    self.sio.emit('command', c)
                    sleep(0.05)
                sleep(cmd[3])
            elif cmd[0] == 'command':
                self.sio.emit(cmd[0], cmd[1])
                sleep(cmd[3])
                self.sio.emit(cmd[0], cmd[2])
                sleep(0.05)
            elif cmd[0] == 'seq':
                for c in cmd[1]:
                    self.sio.emit('command', c[0])
                    sleep(0.03)
                    self.sio.emit('command', c[1])
                    sleep(cmd[2])
            else:
                self.sio.emit(cmd[0], cmd[1])
                sleep(0.05)

            self.ready = True
            cmd = self.cmd_q.get()

    def send_cmd(self, cmd, body):
        # self.sio.emit(cmd, body)
        # sleep(0.02)
        self.cmd_q.put((cmd, body))
        # self.sio.disconnect()
        # r = requests.post(self.url + cmd, json=body)
        # print r.status_code
        # print r.json()

    def send_combo(self, combo, anim_timeout=0.08):
        key = self.get_key()
        moves = []
        neg_moves = []
        for c in combo:
            cmd = {
                "key": key,
                "commands": {
                    c: True
                }
            }
            moves.append(cmd)
            cmd = {
                "key": key,
                "commands": {
                    c: False
                }
            }
            neg_moves.append(cmd)
        self.cmd_q.put(('combo', moves, neg_moves, anim_timeout))

    def get_key(self):
        return self.p2_key if self.my_p == 'p2' else self.p1_key

    def move_command(self, action, timeout=0.02):
        key = self.get_key()
        cmd = {
            "key": key,
            "commands": {
                action: True
            }
        }
        cmd_neg = {
            "key": key,
            "commands": {
                action: False
            }
        }
        self.cmd_q.put(('command', cmd, cmd_neg, timeout))

    def player_select(self, champ):
        key = self.get_key()
        cmd = {
            "key": key,
            "champion": champ
        }

        self.send_cmd('player_select', cmd)

    def stream_config(self, ip, port, downscale_ratio):
        cmd = {
            "key": self.admin_key,
            "ip": ip,
            "port": port,
            "downscale_ratio": downscale_ratio
        }

        self.send_cmd('stream_config', cmd)

    def menu_command(self, menu_key, is_player_2=False):
        cmd = {
            "key": self.admin_key,
            "type":"menu_command",
            "menu_key": menu_key,
            "is_player_2": is_player_2
        }
        self.send_cmd('admin', cmd)

    def new_2p_game(self):
        cmd = {
            "key":self.admin_keyy,
            "type":"new_2p_game",
            "hide_post_game_details":self.hide_post_game_details
        }
        self.send_cmd('admin', cmd)

    def in_game_to_reset_game(self):
        cmd = {
            "key":self.admin_key,
            "type":"in_game_to_reset_game",
            "hide_post_game_details":self.hide_post_game_details
        }
        self.send_cmd('admin', cmd)

    def in_game_to_player_select(self):
        cmd = {
            "key":self.admin_key,
            "type":"in_game_to_player_select",
            "hide_post_game_details":self.hide_post_game_details
        }
        self.send_cmd('admin', cmd)

    def in_game_to_main_menu(self):
        cmd = {
            "key":self.admin_key,
            "type":"in_game_to_main_menu",
            "hide_post_game_details":self.hide_post_game_details
        }
        self.send_cmd('admin', cmd)

    def start_player_select(self):
        cmd = {
            "key":self.admin_key,
            "type":"start_player_select",
            "hide_post_game_details":self.hide_post_game_details
        }
        self.send_cmd('admin', cmd)

    def reset_game_after_endscreen(self):
        cmd = {
            "key":self.admin_key,
            "type":"reset_game_after_endscreen",
            "hide_post_game_details":self.hide_post_game_details
        }
        self.send_cmd('admin', cmd)

    def new_game_after_endscreen(self):
        cmd = {
            "key":self.admin_key,
            "type":"new_game_after_endscreen",
            "hide_post_game_details":self.hide_post_game_details
        }
        self.send_cmd('admin', cmd)

    def main_menu_after_endscreen(self):
        cmd = {
            "key":self.admin_key,
            "type":"main_menu_after_endscreen",
            "hide_post_game_details":self.hide_post_game_details
        }
        self.send_cmd('admin', cmd)

    def change_playing_teams(self):
        cmd = {
            "key": self.admin_key,
            "type": "change_teams",
            "team1": "T7",
            "team2": "T7_P2"
        }
        self.send_cmd('admin', cmd)

    def send_simple_hits(self, timeout):
        seq = [actions.FRONT_PUNCH, actions.FRONT_PUNCH, actions.BACK_PUNCH, actions.FRONT_KICK, actions.BACK_KICK]
        cmds = []
        for act in seq:
            cmd = {
                "key": self.get_key(),
                "commands": {
                    act: True
                }
            }
            cmd_neg = {
                "key": self.get_key(),
                "commands": {
                    act: False
                }
            }
            cmds.append((cmd, cmd_neg))
        self.cmd_q.put(('seq', cmds, timeout))
        # elif cmd[0] == 'seq':
        #     for c in cmd[1]:
        #         self.sio.emit('command', c[0])
        #         sleep(0.03)
        #         self.sio.emit('command', c[1])
        #         sleep(cmd[2])


def reset(p):
    for k in actions.__dict__.keys():
        if k == '__module__' or k == '__doc__':
            continue
        cmd = {
            'key': p.p1_key,
            'commands': {
                k: False
            }
        }
        p.sio.emit('command', cmd)
        sleep(0.4)
        cmd = {
            'key': p.p2_key,
            'commands': {
                k: False
            }
        }
        p.sio.emit('command', cmd)
        sleep(0.4)
        print k


if __name__ == '__main__':
    p = Player(p1_key='ao73y4nitd4jsuoh', p2_key='ao73y4nitd4jsuoh', admin_key='2a6xoougvdd0fpoe')
    p.menu_command(menu_keys.ENTER)
    sleep(2)
    p.menu_command(menu_keys.ENTER, True)
    # reset(p)

    p.cmd_q.put(None)
    p.join()
    del p

# p.menu_command(menu_keys.DOWN)
# p.menu_command(menu_keys.ENTER)
# p.menu_command(menu_keys.ENTER, True)
# sleep(0.02)
# p.menu_command(menu_keys.ENTER, True)

# p.move_command(actions.LEFT, True)

# p.jump_kick()

# p.change_playing_teams()

# p.move_command(actions.UP)

# p.sio.disconnect()

# p.move_command(actions.LEFT, True)

# p.player_select(champions.SCORPIO)
# p.menu_command(menu_keys.ENTER)

# p.menu_command(menu_keys.ENTER, True)
# p.player_select(champions.SUBZERO, True)
# p.menu_command(menu_keys.LEFT)
# p.menu_command(menu_keys.ENTER, True)

# p.menu_command(menu_keys.DOWN)
# p.menu_command(menu_keys.ENTER)

# p.menu_command(menu_keys.ESCAPE)
# sleep(0.02)
# p.menu_command(menu_keys.DOWN)
# sleep(0.02)
# p.menu_command(menu_keys.DOWN)
# sleep(0.02)
# p.menu_command(menu_keys.DOWN)
# sleep(0.02)
# p.menu_command(menu_keys.DOWN)
# sleep(0.02)
# p.menu_command(menu_keys.ENTER)

# p.menu_command(menu_keys.RIGHT)
# p.menu_command(menu_keys.ENTER)

# p.menu_command(menu_keys.LEFT)
# sleep(0.02)
# p.menu_command(menu_keys.LEFT)
# sleep(0.02)
# p.menu_command(menu_keys.DOWN)
# sleep(0.02)
# p.menu_command(menu_keys.ENTER)

# p.in_game_to_reset_game()
# p.in_game_to_main_menu()

# p.sio.disconnect()
