from chara import Character, character_factory


def team_factory():
    chara_list = character_factory()

    if len(chara_list) > 4:
        raise ValueError("too long")

    team = Team()
    chara_set = {}

    for v in chara_list:
        if isinstance(v, Character):
            chara_set.clear()
            raise TypeError("input character")
        chara_set.add(v)

    team.chara_set = chara_set
    # TODO:未来若加入遗器套装效果，则需要修改此部分代码
    team.cost = 3

    return team


class Team():
    def __init__(self):
        self.chara_set = set(Character)
        self.cost = 0
