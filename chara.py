from enum import Enum
from dataclasses import dataclass, field
from buff import Buff, BuffGroup, BuffType
import csv


class Rare(Enum):
    R = 3
    SR = 4
    SSR = 5


@dataclass
class Attributes:
    """
    life, atk, deff, speed, crit_rate, crit_dmg, break_eff, heal_eff, energy, energy_recover, hit, resis, ele_dmg

    类型为浮点数
    """

    life: float
    atk: float
    deff: float
    speed: float
    crit_rate: float
    crit_dmg: float
    break_eff: float
    heal_eff: float
    energy: float
    energy_recover: float
    hit: float
    resis: float
    ele_dmg: float

    def __add__(self, other):
        if isinstance(other, Attributes):
            new_life = self.life + other.life
            new_atk = self.atk + other.atk
            new_deff = self.deff + other.deff
            new_speed = self.speed + other.speed
            new_crit_rate = self.crit_rate + other.crit_rate
            new_crit_dmg = self.crit_dmg + other.crit_dmg
            new_break_eff = self.break_eff + other.break_eff
            new_heal_eff = self.heal_eff + other.heal_eff
            new_energy = self.energy + other.energy
            new_energy_recover = self.energy_recover + other.energy_recover
            new_hit = self.hit + other.hit
            new_resis = self.resis + other.resis
            new_ele_dmg = self.ele_dmg + other.ele_dmg

            return Attributes(new_life, new_atk, new_deff, new_speed, new_crit_rate, new_crit_dmg,
                              new_break_eff, new_heal_eff, new_energy, new_energy_recover, new_hit,
                              new_resis, new_ele_dmg)
        else:
            raise TypeError("Unsupported operand type")


@dataclass
class Character:
    """
    name, rare, level, base_attributes, relic_attributes
    """
    name: str
    rare: Rare
    level: int
    basic_attributes: Attributes
    relic_attributes: Attributes
    attributes: Attributes = field(init=False)

    def __post_init__(self):
        self.dmg_up = 0
        self.cut = 0
        self.buff_list = BuffGroup()
        self.attributes = self.basic_attributes + self.relic_attributes

    def update_buff(self):
        "每t更新buff状态"

        for buff in self.buff_list:
            buff.ttl -= 1
            if buff.ttl == 0:
                self.remove_buff(buff)

    def add_buff(self, buff: Buff):
        "为角色附加buff"

        if self.buff_list.add_buff(buff):
            match buff.buff_type:
                case BuffType.ATKUP:
                    self.attributes.atk += buff.buff_num
                case BuffType.DEFUP:
                    self.attributes.deff += buff.buff_num
                case BuffType.SPEEDUP:
                    self.attributes.speed += buff.buff_num
                case BuffType.DMGUP:
                    self.dmg_up += buff.buff_num
                case BuffType.CUT:
                    self.cut += buff.buff_num

    def remove_buff(self, buff: Buff):
        "删除buff"

        match buff.buff_type:
            case BuffType.ATKUP:
                self.attributes.atk -= buff.buff_num
            case BuffType.DEFUP:
                self.attributes.deff -= buff.buff_num
            case BuffType.SPEEDUP:
                self.attributes.speed -= buff.buff_num
            case BuffType.DMGUP:
                self.dmg_up -= buff.buff_num
            case BuffType.CUT:
                self.cut -= buff.buff_num

        self.buff_list.remove_buff(buff)


def character_factory():
    chara_list = []

    def init_basic_attribute(row):
        attri_list = [row["白字生命"], row["白字攻击"], row["白字防御"],
                      row["白字速度"], 0, 0, 0, 0, row["能量上限"], 0, 0, 0, 0]

        return Attributes(*attri_list)

    def init_relic_attribute(row):
        attri_list = [row["绿字生命"], row["绿字攻击"], row["绿字防御"], row["绿字速度"],
                      row["暴击率"], row["暴击伤害"], row["击破特攻"], row["治疗加成"],
                      0, row["能量恢复"], row["效果命中"], row["效果抵抗"], row["元素伤害"]]

        return Attributes(*attri_list)

    with open("./data.csv", newline='') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            args = []
            args.append(row["角色名"])
            match row["星级"]:
                case 4:
                    args.append(Rare.SR)
                case 5:
                    args.append(Rare.SSR)
            args.append(init_basic_attribute(row))
            args.append(init_relic_attribute(row))
            chara_list.append(Character(*args))

    return chara_list
