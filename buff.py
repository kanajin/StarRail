from enum import Enum, auto
from dataclasses import dataclass


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
    def __init__(self):
        self.buff_dict = dict()

    def add_buff(self, buff: Buff) -> bool:
        "返回True表示添加了一个新的buff，返回False表示已有该buff，刷新持续时间"

        if self.buff_dict.get((buff.buff_from, buff.buff_id)):
            self.buff_dict[(buff.buff_from, buff.buff_id)].ttl = buff.ttl
            return False
        else:
            self.buff_dict[(buff.buff_from, buff.buff_id)] = buff
            return True

    def remove_buff(self, buff: Buff):
        del self.buff_dict[(buff.buff_from, buff.buff_id)]
