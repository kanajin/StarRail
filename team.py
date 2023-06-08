from chara import Character, character_list_factory
from enum_classes import CharacterID

def team_factory():
    chara_list = character_list_factory()

    if len(chara_list) > 4:
        raise ValueError("too long")

    team = Team()

    team.chara_list = chara_list
    # TODO:未来若加入遗器套装效果，则需要修改此部分代码
    team.cost = 3

    return team


class Team():
    def __init__(self):
        self.chara_list = []
        self.cost = 0

    def get_chara(self, id):
        for chara in self.chara_list:
            if chara.id == id:
                return chara
            
        return None
