import copy
import random


class Doc(object):
    def draw(self):
        pass

    def copy(self):
        return copy.deepcopy(self)

    def mutate(self, r):
        cop = self.copy()
        for prop, val in cop.__dict__.items():
            if "mutate" in dir(val):
                cop.__setattr__(prop, val.mutate(r))
        return cop


class Proxy(object):
    def __init__(self, obj, mutate):
        self._mut = mutate
        self.v = obj

    def mutate(self, r):
        return Proxy(self._mut(self.v, r), self._mut)


class Tuproxy(object):
    def __init__(self, vals, mutate):
        self._mut = mutate
        self.v = vals

    def mutate(self, r):
        return Tuproxy(tuple(self._mut(y, r) for y in self.v), self._mut)


def tuproxy(n, init, mutate):
    return Tuproxy(tuple(copy.deepcopy(init) for _ in range(n)), mutate)


def randint(num, start=0):
    def mutate(self, r):
        s = int((num - start) * r)
        self = self + random.randrange(-s, s)
        if self < start:
            self = start
        if self >= num:
            self = num - 1
        return self
    return mutate


def choice(choices):
    def mutate(self, r):
        if random.random() < r:
            return random.randrange(0, choices)
        return self
    return mutate
