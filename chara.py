from dataclasses import dataclass,field
from enum_classes import AttributeID,CharacterID
import csv
from buff import BuffGroup


@dataclass
class Attribute:
    id: AttributeID
    value: int
    

class AttributeList:
    def __init__(self):
        self.attributes = {}

        self.attributes[AttributeID.LEVEL] = Attribute(AttributeID.LEVEL, 0) # 等级
        self.attributes[AttributeID.BASE_HEALTH] = Attribute(AttributeID.BASE_HEALTH, 0)  # 基础生命值
        self.attributes[AttributeID.PERTH_HEALTH] = Attribute(AttributeID.PERTH_HEALTH, 0)  # 百分比生命值
        self.attributes[AttributeID.EXTRA_HEALTH] = Attribute(AttributeID.EXTRA_HEALTH, 0)  # 额外生命值
        self.attributes[AttributeID.BASE_ATTACK] = Attribute(AttributeID.BASE_ATTACK, 0)  # 基础攻击力
        self.attributes[AttributeID.PERTH_ATTACK] = Attribute(AttributeID.PERTH_ATTACK, 0)  # 百分比攻击力
        self.attributes[AttributeID.EXTRA_ATTACK] = Attribute(AttributeID.EXTRA_ATTACK, 0)  # 额外攻击力
        self.attributes[AttributeID.BASE_DEFENSE] = Attribute(AttributeID.BASE_DEFENSE, 0)  # 基础防御力
        self.attributes[AttributeID.PERTH_DEFENSE] = Attribute(AttributeID.PERTH_DEFENSE, 0)  # 百分比防御力
        self.attributes[AttributeID.EXTRA_DEFENSE] = Attribute(AttributeID.EXTRA_DEFENSE, 0)  # 额外防御力
        self.attributes[AttributeID.BASE_SPEED] = Attribute(AttributeID.BASE_SPEED, 0)  # 基础速度
        self.attributes[AttributeID.PERTH_SPEED] = Attribute(AttributeID.PERTH_SPEED, 0)  # 百分比速度
        self.attributes[AttributeID.EXTRA_SPEED] = Attribute(AttributeID.EXTRA_SPEED, 0)  # 额外速度
        self.attributes[AttributeID.CRITICAL_CHANCE] = Attribute(AttributeID.CRITICAL_CHANCE, 0)  # 暴击
        self.attributes[AttributeID.CRITICAL_DAMAGE] = Attribute(AttributeID.CRITICAL_DAMAGE, 0)  # 暴击伤害
        self.attributes[AttributeID.BREAK_ATTACK] = Attribute(AttributeID.BREAK_ATTACK, 0)  # 击破特攻
        self.attributes[AttributeID.HEAL_BONUS] = Attribute(AttributeID.HEAL_BONUS, 0)  # 治疗量加成
        self.attributes[AttributeID.ENERGY_LIMIT] = Attribute(AttributeID.ENERGY_LIMIT, 0)  # 能量上限
        self.attributes[AttributeID.ENERGY_RECOVERY] = Attribute(AttributeID.ENERGY_RECOVERY, 0)  # 能量恢复效率
        self.attributes[AttributeID.CURRENT_ENERGY] = Attribute(AttributeID.CURRENT_ENERGY, 0)  # 当前能量
        self.attributes[AttributeID.EFFECT_HIT] = Attribute(AttributeID.EFFECT_HIT, 0)  # 效果命中
        self.attributes[AttributeID.EFFECT_RESIST] = Attribute(AttributeID.EFFECT_RESIST, 0)  # 效果抵抗
        self.attributes[AttributeID.ATTRIBUTE_DAMAGE] = Attribute(AttributeID.ATTRIBUTE_DAMAGE, 0)  # 属性伤害提高
        self.attributes[AttributeID.DAMAGE_INCREASE] = Attribute(AttributeID.DAMAGE_INCREASE, 0)  # 增伤
        self.attributes[AttributeID.ADDITIONAL_DAMAGE] = Attribute(AttributeID.ADDITIONAL_DAMAGE, 0)  # 追加伤害增伤
        self.attributes[AttributeID.STACK] = Attribute(AttributeID.STACK, 0)  # 命座


@dataclass
class Character:
    id: CharacterID
    attributes: AttributeList = field(init=False)
    buff_list: BuffGroup = field(init=False)

    def __post_init__(self):
        self.attributes = AttributeList()
        self.buff_list = BuffGroup()

    def get_attr(self, id):
        return self.attributes.attributes[id]
    
    def increase_attr(self, id, value):
        old_value = self.get_attr(id)
        self.set_attr(id, old_value+value)
    
    def set_attr(self, id, value):
        self.attributes.attributes[id] = value

    def sub_attr(self, id, value):
        self.attributes.attributes[id] -= value

    def get_atk(self):
        atk = self.get_attr(AttributeID.BASE_ATTACK)*(1000+self.get_attr(AttributeID.PERTH_ATTACK))/1000+self.get_attr(AttributeID.EXTRA_ATTACK)
        return atk
    
    def get_speed(self):
        speed = self.get_attr(AttributeID.BASE_SPEED)*(1000+self.get_attr(AttributeID.PERTH_SPEED))/1000+self.get_attr(AttributeID.EXTRA_SPEED)
        return speed



def character_list_factory():
    charaters = []

    with open("./character.csv",newline='',encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            chara = Character(CharacterID(row[0]))

            for i in range(1,len(header)):
                attr_id = AttributeID(header[i])
                attr_value = int(row[i])

                if attr_id in chara.attributes.attributes:
                    chara.set_attr(attr_id,int(attr_value))

            charaters.append(chara)

    return charaters


character_list = character_list_factory()