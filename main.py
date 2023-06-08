from fight import Fight

if __name__ == '__main__':
    f = Fight(1)
    f.fight()

    total_dmg = 0
    dmg_distribute = [0, 0, 0, 0, 0, 0]
    for data in f.dmg_list:
        total_dmg += data[2]
        dmg_distribute[data[0]-1] += data[2]
    for i, data in enumerate(f.cost_list):
        print(f'第{i}轮战技点情况：{data}')
    
    print(f'总伤害{total_dmg}。')
    for i,dmg in enumerate(dmg_distribute):
        dmg_type = ''
        match i+1:
            case 1:
                dmg_type = '景元普攻'
            case 2:
                dmg_type = '景元E'
            case 3:
                dmg_type = '景元大'
            case 4:
                dmg_type = '神君'
            case 5:
                dmg_type = '停云普攻'
            case 6: 
                dmg_type = '停云普攻追伤'

        print(f'{dmg_type}的伤害总量{dmg}，占比{dmg/total_dmg*100}%，')

    print(f'战斗总计：停云行动{f.tingyunxingdong}次，景元行动{f.jingyuanxingdong}次，开大{f.jingyuankaida}次，神君行动{f.shenjunxingdong}次')
