from enum_classes import AttributeID


def crit_fix(chara, dmg):
    crit_chance = chara.get_attr(AttributeID.CRITICAL_CHANCE)
    crit_dmg = chara.get_attr(AttributeID.CRITICAL_DAMAGE)

    fix_dmg = dmg*(1000000 + crit_chance*crit_dmg)
    return fix_dmg/1000000


def def_effect(chara):
    coefficient = chara.get_attr(AttributeID.LEVEL)*10 + 200
    return coefficient/(coefficient+1100)


def total_atk(chara):
    return (chara.get_attr(
            AttributeID.BASE_ATTACK)*(1000+chara.get_attr(AttributeID.PERTH_ATTACK))/1000
            + chara.get_attr(AttributeID.EXTRA_ATTACK))


class BuffEffectType:
    def numeric_up(self, buff, id, value):
        owner = buff.owner
        owner.increase_attr(AttributeID(str(id)), value)

    def tingyun_e_atk_buff(self, buff, atkup, atkrooft):
        owner = buff.owner
        creator = buff.creator

        atk_up = min(total_atk(creator)*atkrooft/1000,
                     owner.get_attr(AttributeID.BASE_ATTACK)*atkup/1000)

        return atk_up

    def energy_recover(self, buff, value):
        owner = buff.owner

        owner.set_attr(AttributeID.CURRENT_ENERGY, min(owner.get_attr(
            AttributeID.CURRENT_ENERGY)+value, owner.get_attr(AttributeID.ENERGY_LIMIT)))


class DMGEffectType:
    def cause_dmg_mul(self, chara, mag, increase=0):
        return total_atk(chara)*mag*(1000+chara.get_attr(AttributeID.DAMAGE_INCREASE)+chara.get_attr(AttributeID.ATTRIBUTE_DAMAGE)+increase)*def_effect(chara)/1000000

    def tingyun_talent_dmg(self, buff, mag):
        if buff.creator.get_attr(AttributeID.STACK) >= 4:
            mag += 200

        owner = buff.owner

        extra_dmg = self.cause_dmg_mul(owner, mag, 150)

        return crit_fix(owner, extra_dmg)
