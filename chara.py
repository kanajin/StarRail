from enum import Enum,auto
from dataclasses import dataclass, field


class Rare(Enum):
    R = 3
    SR = 4
    SSR = 5

class BuffType(Enum):
    ATKUP = auto()
    DEFUP = auto()
    SPEEDUP = auto()
    DMGUP = auto()
    CUT = auto()
    
@dataclass
class Buff():
    """buff_from, buff_id, buff_type, buff_effect, ttl, buff_num
    
    buff_from 表示buff来源角色，buff_id 表示buff为该角色哪个技能，普攻-1，战技-2，大招-3，秘技-4，用于同类型buff的覆盖

    buff_effct 表示buff提升幅度，单位为百分比

    buff_num 表示计算后的buff实际数值，用于角色数值变化
    """
    buff_from: str
    buff_id: int
    buff_type: BuffType
    buff_effect: float
    ttl: int
    buff_num = 0

class BuffGroup():
    buff_dict = dict()

    def add_buff(self, buff: Buff) -> bool:
        "返回True表示添加了一个新的buff，返回False表示已有该buff，刷新持续时间"

        if self.buff_dict.get((buff.buff_from, buff.buff_id)):
            self.buff_dict[(buff.buff_from, buff.buff_id)].ttl = buff.ttl
            return False
        else:
            self.buff_dict[(buff.buff_from, buff.buff_id)] = buff
            return True
        
    def remove_buff(self, buff:Buff):
        del self.buff_dict[(buff.buff_from, buff.buff_id)]

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

class Character:
    """
    name, rare, base_attributes, relic_attributes
    """
    name: str
    rare: Rare
    basic_attributes: Attributes
    relic_attributes: Attributes
    dmg_up = 0
    cut = 0
    buff_list = BuffGroup()
    attributes: Attributes = field(init=False)

    def __post_init__(self):
        self.attributes = self.basic_attributes + self.relic_attributes

    def update_buff(self):
        "每t更新buff状态"

        for buff in self.buff_list:
            buff.ttl -= 1
            if buff.ttl == 0:
                self.remove_buff(buff)

    def add_buff(self,buff:Buff):
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

    def remove_buff(self,buff:Buff):
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
