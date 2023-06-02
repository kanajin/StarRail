import heapq
from team import team_factory


class Runner:
    def __init__(self, action_value, name):
        self.action_value = action_value
        self.name = name

    def __lt__(self, other):
        return self.action_value < other.action_value


class ActList:
    def __init__(self):
        self.queue = []
        self.idx = 0

    def push(self, runner: Runner):
        heapq.heappush(self.queue, (runner.action_value, self.idx, runner))
        self.idx += 1

    def pop(self):
        return heapq.heappop(self.queue)[2]

    def reset_idx(self):
        self.idx = 0


class Fight:
    def __init__(self):
        self.team = team_factory()
        self.act_list = ActList()

        runner_list = [Runner(15000/x.attributes.speed, x.name)
                       for x in self.team.chara_set]
        runner_list.append(Runner(150, "default_runner"))

        [self.act_list.push(runner) for runner in runner_list]

    def chara_action():