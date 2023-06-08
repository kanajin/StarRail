from dataclasses import dataclass
from effect import BuffEffectType
from enum_classes import AttributeID


class Buff:
    def __init__(self, id, creator, owner, ttl, attr_id, value, stack=0, is_this_turn=False):
        self.id = id
        self.creator = creator
        self.owner = owner
        self.ttl = ttl
        self.attr_id = attr_id
        self.value = value
        self.stack = stack
        self.is_this_turn = is_this_turn


class BuffGroup:
    def __init__(self):
        self.buff_dict = dict()

    def contains(self, id):
        if self.buff_dict.get(id):
            return True
        return False

    def get_buff(self, id):
        return self.buff_dict.get(id)

    def add_buff(self, buff: Buff):
        if self.contains(buff.id):
            self.buff_dict[buff.id].ttl = buff.ttl
            return False
        else:
            self.buff_dict[buff.id] = buff
            return True

    def remove_buff(self, buff: Buff):
        del self.buff_dict[buff.id]


class BuffConfig:
    def __init__(self):
        self.buff_effect_type = BuffEffectType()

    def tingyun_E(self, creator, owner):
        buff = Buff('1001', creator, owner, 3,
                    AttributeID.EXTRA_ATTACK, 0)
        atk_up = self.buff_effect_type.tingyun_e_atk_buff(buff, 500, 250)
        buff.value = atk_up
        if owner.buff_list.add_buff(buff):
            owner.set_attr(AttributeID.EXTRA_ATTACK, owner.get_attr(
                AttributeID.EXTRA_ATTACK)+atk_up)

    def tingyun_Q(self, creator, owner):
        buff = Buff('1002', creator, owner, 2,
                    AttributeID.DAMAGE_INCREASE, 500)
        if owner.buff_list.add_buff(buff):
            self.buff_effect_type.numeric_up(buff, 92, 500)
        if creator.get_attr(AttributeID.STACK) >= 6:
            self.buff_effect_type.energy_recover(buff, 60)
        else:
            self.buff_effect_type.energy_recover(buff, 50)

    def jingyuan_xingji(self, creator, owner):
        buff = Buff('1004', creator, owner, 2,
                    AttributeID.CRITICAL_CHANCE, 100)
        if owner.buff_list.add_buff(buff):
            self.buff_effect_type.numeric_up(buff, 42, 100)

    def jizou_atk_up(self, creator, owner):
        buff = Buff('1005', creator, owner, 1, AttributeID.PERTH_ATTACK, 200)
        if owner.buff_list.add_buff(buff):
            self.buff_effect_type.numeric_up(buff, 12, 200)

    def mengshen(self, creator, owner):
        buff = Buff('1006', creator, owner, -1,
                    AttributeID.ADDITIONAL_DAMAGE, 0, 1)
        if owner.buff_list.add_buff(buff):
            self.buff_effect_type.numeric_up(buff, 93, 0)

    def tingyun_E_speed_up(self, creator, owner):
        buff = Buff('1007', creator, owner, 1, AttributeID.PERTH_SPEED, 200)
        if owner.buff_list.add_buff(buff):
            self.buff_effect_type.numeric_up(buff, 32, 200)

    def tingyun_xingji_speed_up(self, creator, owner):
        buff = Buff('1008', creator, owner, 1, AttributeID.PERTH_SPEED, 200)
        if owner.buff_list.add_buff(buff):
            self.buff_effect_type.numeric_up(buff, 32, 200)
