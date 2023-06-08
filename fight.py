import heapq
from team import team_factory
from enum_classes import CharacterID,AttributeID
from buff import BuffConfig
from summoner import Shenjun
from effect import DMGEffectType,crit_fix,def_effect
import random

def actlist_factory(chara_list):
    """约定：

    角色id即为此处id，不过此处类型为int

    默认单位id为0，神君id为-1
    """
    actlist = ActList()

    runner_list = [(10000/chara.get_speed(), chara.id.to_int(chara.id))
                   for chara in chara_list]

    runner_list.append((150, 0))

    [actlist.push(*runner) for runner in runner_list]

    return actlist


class ActList:
    def __init__(self):
        self.queue = []
        self.idx = 0

    def push(self, action_value, id):
        heapq.heappush(self.queue, [action_value, self.idx, id])
        self.idx += 1

    def pop(self):
        return heapq.heappop(self.queue)

    def peek(self):
        if self.queue:
            return self.queue[0]
        else:
            return None

    def get_ele_by_id(self, id):
        for ele in self.queue:
            if ele[2] == id:
                return ele
        return None
    
    def get_idx_by_id(self, id):
        for idx, ele in self.queue:
            if ele[2] == id:
                return idx
    
    def get_action_value_by_id(self, id):
        return self.get_ele_by_id(id)[0]

    def update_action_value(self, id, new_value):
        ele = self.get_ele_by_id(id)
        ele[0] = new_value
        heapq.heapify(self.queue)

    def reset_idx(self):
        self.idx = 0

    def next_runner(self):
        spend = self.peek()[0]
        for ele in self.queue:
            ele[0] -= spend
        """
        ele_list = []
        for ele in self.queue:
            ele_list.append(ele)
        self.queue.clear()
        for ele in ele_list:
            self.push(ele[0]-spend,ele[2])
        """


class Fight:
    def __init__(self, enemy_num):
        self.team = team_factory()
        self.act_list = actlist_factory(self.team.chara_list)
        self.shenjun = Shenjun()
        self.buff_config = BuffConfig()
        self.dmg_effect = DMGEffectType()
        self.dmg_list = []
        self.cost_list = []
        self.enemy_num = enemy_num
        self.round = 1
        self.act_list.push(10000/60,-1)
        self.jingyuanxingdong = 0
        self.tingyunxingdong = 0
        self.shenjunxingdong = 0
        self.jingyuankaida = 0

    def curr_chara(self):
        """返回正在行动的单位id
        """
        if self.act_list.peek()[0] != 0:
            self.act_list.next_runner()

        return self.act_list.peed()[2]

    def recal_action_value_and_update(self, id, old_speed, new_speed):
        curr_action_value = self.act_list.get_ele_by_id(id)[0]
        new_action_value = curr_action_value*old_speed/new_speed
        self.act_list.update_action_value(id, new_action_value)

    def end_round(self):
        print('---轮次结束---')
        self.act_list.push(100,0)
        self.act_list.reset_idx()
        self.cost_list.append(self.team.cost)
        self.round += 1

    def end_turn(self):
        ele = self.act_list.pop()
        match ele[2]:
            case 0: # 默认单位，表示一轮已经结束
                self.end_round()
            case -1: # 神君
                self.shenjun.reset()
                self.act_list.push(10000/self.shenjun.speed,-1)
            case _:
                chara = self.team.get_chara(CharacterID(str(ele[2])))
                self.act_list.push(10000/chara.get_speed(),ele[2])
                remove_buff_list = []
                for buff in chara.buff_list.buff_dict.values():
                    if buff.is_this_turn:
                        buff.is_this_turn = False
                        continue
                    elif buff.ttl > 0:
                        buff.ttl -= 1
                        if buff.ttl == 0:
                            remove_buff_list.append(buff)

                for buff in remove_buff_list:
                    chara.buff_list.remove_buff(buff)
                    chara.sub_attr(buff.attr_id,buff.value)

    def record_dmg(self, id, dmg):
        self.dmg_list.append((id,self.round,dmg))

    def chara_recover_energy(self, chara, value):
        chara.set_attr(AttributeID.CURRENT_ENERGY, min(chara.get_attr(
            AttributeID.CURRENT_ENERGY)+value*(1000+chara.get_attr(AttributeID.ENERGY_RECOVERY))/1000, chara.get_attr(AttributeID.ENERGY_LIMIT)))


    def tingyun_action(self):
        self.tingyunxingdong += 1
        print('停云行动: ',end='')
        tingyun = self.team.get_chara(CharacterID.TINGYUN)
        self.chara_recover_energy(tingyun, 5)

        def try_big():
            if tingyun.get_attr(AttributeID.CURRENT_ENERGY) == tingyun.get_attr(AttributeID.ENERGY_LIMIT):
                print('停云开大')
                self.buff_config.tingyun_Q(tingyun, self.team.get_chara(CharacterID.JINGYUAN))
                tingyun.set_attr(AttributeID.CURRENT_ENERGY,5)

        def use_E():
            print('停云战技')
            self.buff_config.tingyun_E(tingyun,self.team.get_chara(CharacterID.JINGYUAN))
            self.buff_config.tingyun_xingji_speed_up(tingyun,tingyun)
            tingyun.buff_list.get_buff('1008').is_this_turn = True
            self.chara_recover_energy(tingyun,30)
            self.team.cost -= 1

        def use_Q():
            print('停云普攻')
            q_dmg = self.dmg_effect.cause_dmg_mul(tingyun, 1000)
            self.record_dmg(5,crit_fix(tingyun,q_dmg))
            ex_dmg = self.dmg_effect.tingyun_talent_dmg(buff, 600)
            self.record_dmg(6,crit_fix(tingyun,ex_dmg))
            self.chara_recover_energy(tingyun,24)
            self.team.cost += 1

        try_big()

        if self.team.get_chara(CharacterID.JINGYUAN).buff_list.contains('1001'):
            buff = self.team.get_chara(CharacterID.JINGYUAN).buff_list.get_buff('1001')
            if buff.ttl < 2:
                if self.act_list.get_action_value_by_id(1) < self.act_list.get_action_value_by_id(-1):
                    use_E()
            else:
                use_Q()
        else:
            use_E()



    def jingyuan_action(self):
        self.jingyuanxingdong += 1
        jingyuan = self.team.get_chara(CharacterID.JINGYUAN)
        total_atk = (jingyuan.get_attr(
            AttributeID.BASE_ATTACK)*(1000+jingyuan.get_attr(AttributeID.PERTH_ATTACK))/1000
            + jingyuan.get_attr(AttributeID.EXTRA_ATTACK))
        print(f'景元行动（攻击力:{total_atk}）：',end='')

        def try_mengshen():
            if not jingyuan.buff_list.contains('1006'):
                self.buff_config.mengshen(jingyuan,jingyuan)

        def try_big():
            if jingyuan.get_attr(AttributeID.CURRENT_ENERGY) == jingyuan.get_attr(AttributeID.ENERGY_LIMIT):
                self.jingyuankaida += 1
                print('景元开大')
                try_mengshen()
                dmg = self.dmg_effect.cause_dmg_mul(jingyuan,2000,330)*self.enemy_num
                self.record_dmg(3,crit_fix(jingyuan,dmg))
                if self.team.get_chara(CharacterID.TINGYUN).get_attr(AttributeID.STACK) >= 1 and jingyuan.buff_list.contains('1001'):
                    self.buff_config.tingyun_E_speed_up(self.team.get_chara(CharacterID.TINGYUN),jingyuan)
                    jingyuan.buff_list.get_buff('1007').is_this_turn = True
                
                self.recal_action_value_and_update(-1,self.shenjun.atk_times_up(3),self.shenjun.speed)
                
                jingyuan.set_attr(AttributeID.CURRENT_ENERGY,5)
        
        def use_E():
            print('景元战技')
            try_mengshen()
            dmg = self.dmg_effect.cause_dmg_mul(jingyuan,1000,180)*self.enemy_num
            self.record_dmg(2,crit_fix(jingyuan,dmg))
            self.buff_config.jingyuan_xingji(jingyuan,jingyuan)
            jingyuan.buff_list.get_buff('1004').is_this_turn = True
            self.buff_config.jizou_atk_up(jingyuan,jingyuan)
            jingyuan.buff_list.get_buff('1005').is_this_turn = True

            self.team.cost -= 1
            self.recal_action_value_and_update(-1,self.shenjun.atk_times_up(2),self.shenjun.speed)

            self.chara_recover_energy(jingyuan,30)

        def use_Q():
            print('景元普攻')
            dmg = self.dmg_effect.cause_dmg_mul(jingyuan,1000)
            self.record_dmg(1,crit_fix(jingyuan,dmg))
            
            self.team.cost += 1

        if self.team.cost > 0:
            use_E()
        else:
            use_Q()

        try_big()

    def shenjun_action(self):
        self.shenjunxingdong += 1
        jingyuan = self.team.get_chara(CharacterID.JINGYUAN)
        total_atk = (jingyuan.get_attr(
            AttributeID.BASE_ATTACK)*(1000+jingyuan.get_attr(AttributeID.PERTH_ATTACK))/1000
            + jingyuan.get_attr(AttributeID.EXTRA_ATTACK))
        print(f'神君行动（段数：{self.shenjun.atk_times}），',end = '')
        print(f'景元攻击：{total_atk}')
        if jingyuan.get_attr(AttributeID.STACK) >= 1:
            self.shenjun.sputt = 500
            
        every_time_dmg = 0
        if jingyuan.buff_list.contains('1006'):
            every_time_dmg = total_atk*660*(1000+jingyuan.get_attr(AttributeID.DAMAGE_INCREASE)+480+150)*def_effect(jingyuan)/1000000
            jingyuan.buff_list.remove_buff(jingyuan.buff_list.get_buff('1006'))
        else:
            every_time_dmg = total_atk*660*(1000+jingyuan.get_attr(AttributeID.DAMAGE_INCREASE)+150)*def_effect(jingyuan)/1000000
        every_time_dmg = crit_fix(jingyuan,every_time_dmg)

        total_dmg = 0

        match self.enemy_num:
            case 1:
                total_dmg = every_time_dmg * self.shenjun.atk_times
            case 2:
                total_dmg = every_time_dmg * (1000+self.shenjun.sputt) * self.shenjun.atk_times/1000
            case 3:
                for i in range(self.shenjun.atk_times-1):
                    target = random.randint(0,self.enemy_num-1)
                    match target:
                        case 1:
                            total_dmg += (1000+2*self.shenjun.sputt)*every_time_dmg/1000
                        case _:
                            total_dmg += (1000+self.shenjun.sputt)*every_time_dmg/1000
            case _:
                raise ValueError('目前最多支持三个敌人捏。。')
            
        self.record_dmg(4, total_dmg)

    def default_action(self):
        self.team.cost += 1
        
    def fight(self):
        while self.round <= 8:
            self.act_list.next_runner()

            match self.act_list.peek()[2]:
                case -1:
                    self.shenjun_action()
                case 0:
                    pass
                case 1:
                    self.jingyuan_action()
                case 2:
                    self.tingyun_action()
                case _:
                    self.default_action()

            self.end_turn()

