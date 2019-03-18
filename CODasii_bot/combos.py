from commands import actions
from random import randint


class ScorpionCombos:
    def __init__(self):
        pass

    @staticmethod
    def teleport(back):
        return [actions.DOWN, back, actions.FRONT_KICK]

    @staticmethod
    def spear(back, forward):
        return [back, forward, actions.FRONT_PUNCH]

    @staticmethod
    def takedown(back, forward):
        return [back, forward, actions.BACK_KICK]

    @staticmethod
    def whoNext_fatal(back, forward):
        return [actions.DOWN, back, forward, actions.UP]

    @staticmethod
    def stopAhead_fatal(back, forward):
        return [actions.DOWN, back, forward, actions.BACK_PUNCH]

    @staticmethod
    def get_random():
        all_combos = [ScorpionCombos.whoNext,
                      ScorpionCombos.stopAhead,
                      ScorpionCombos.klassic,
                      ScorpionCombos.stage]
        return all_combos[randint(0, len(all_combos) - 1)]

    # combo2
    # p.send_combo([actions.DOWN, actions.LEFT, actions.RIGHT, actions.UP])


class SubzeroCombos:
    def __init__(self):
        pass

    @staticmethod
    def hammer(back):
        return [actions.DOWN, back, actions.BACK_PUNCH, actions.BLOCK]

    @staticmethod
    def sword():
        return [actions.DOWN, actions.BACK_PUNCH]

    @staticmethod
    def get_random():
        all_combos = [SubzeroCombos.klassic, SubzeroCombos.stage]
        return all_combos[randint(0, len(all_combos) - 1)]()

    @staticmethod
    def kold_fatal(back, forward):
        return [back, forward, actions.DOWN, back, actions.BACK_KICK]

    @staticmethod
    def bedIce_fatal(back, forward):
        return [actions.DOWN, back, actions.DOWN, forward, actions.BACK_KICK]

    @staticmethod
    def slide(back, forward):
        return [back, forward, actions.BACK_KICK]

    @staticmethod
    def iceBurst(back):
        # hit ground, throw him away
        return [actions.DOWN, back, actions.FRONT_PUNCH]

    @staticmethod
    def iceBall(forward):
        # ice ball / ice hammer
        return [actions.DOWN, forward, actions.BACK_PUNCH]

    @staticmethod
    def klassic():
        return [actions.RIGHT, actions.DOWN, actions.RIGHT, actions.BACK_PUNCH]

    @staticmethod
    def stage():
        return [actions.RIGHT, actions.DOWN, actions.LEFT, actions.BACK_PUNCH]

    @staticmethod
    def cold_blooded(forward):
        return [forward, actions.BACK_KICK, actions.BACK_PUNCH, actions.FRONT_PUNCH]

    @staticmethod
    def slash(forward):
        return [forward, actions.FRONT_PUNCH, actions.BACK_PUNCH]