class Summoner:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed


class Shenjun(Summoner):
    def __init__(self, ):
        self.atk_times = 3
        self.speed = 60
        self.sputt = 250

    def atk_times_up(self, add_num):
        old_atk_times = self.atk_times
        old_speed = self.speed
        self.atk_times = min(self.atk_times+add_num, 10)
        self.speed += (self.atk_times-old_atk_times)*10
        return old_speed

    def reset(self):
        self.speed = 60
        self.atk_times = 3
