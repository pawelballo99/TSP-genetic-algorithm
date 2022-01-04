import random


class Individual:
    def __init__(self, gen_nr):
        self.genome = random.sample(range(1, gen_nr), gen_nr - 1)
        self.cost = 0

    def mutate(self):
        idx1, idx2 = random.randint(0, len(self.genome) - 1), random.randint(0, len(self.genome) - 1)
        start, stop = min(idx1, idx2), max(idx1, idx2)
        self.genome[start:stop].reverse()
