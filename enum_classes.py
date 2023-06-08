from enum import Enum


class AttributeID(Enum):
    LEVEL = '0'
    BASE_HEALTH = '1'
    PERTH_HEALTH = '2'
    EXTRA_HEALTH = '3'
    BASE_ATTACK = '11'
    PERTH_ATTACK = '12'
    EXTRA_ATTACK = '13'
    BASE_DEFENSE = '21'
    PERTH_DEFENSE = '22'
    EXTRA_DEFENSE = '23'
    BASE_SPEED = '31'
    PERTH_SPEED = '32'
    EXTRA_SPEED = '33'
    CRITICAL_CHANCE = '41'
    CRITICAL_DAMAGE = '42'
    BREAK_ATTACK = '51'
    HEAL_BONUS = '61'
    ENERGY_LIMIT = '71'
    ENERGY_RECOVERY = '72'
    CURRENT_ENERGY = '73'
    EFFECT_HIT = '81'
    EFFECT_RESIST = '82'
    ATTRIBUTE_DAMAGE = '91'
    DAMAGE_INCREASE = '92'
    ADDITIONAL_DAMAGE = '93'
    STACK = '101'


class CharacterID(Enum):
    JINGYUAN = '1'
    TINGYUN = '2'
    HUOZHU = '3'
    NAIMA = '4'

    def to_int(self, id):
        match id:
            case self.JINGYUAN:
                return 1
            case self.TINGYUN:
                return 2
            case self.HUOZHU:
                return 3
            case self.NAIMA:
                return 4
