class Player:
    def __init__(self, name, items=None, stats=None):
        self.name = name
        if items is None:
            self.items = []

        if stats is None:
            self.stats = []

        self.stats = {stat.name: stat.value for stat in stats}

    def get_item(item):
        self.items.append(item)
        item.get_hook(self)

    def lose_item(item):
        self.itms.remove(item)
        item.lose_hook(self)

    def stat_check(self, name, target, leq=False):
        cur_val = self.stats[name].value

        if not leq:
            return cur_val >= target
        else:
            return cur_val <= target

class Item(object):
    def __init__(self, name, stacks=False, get_hook=lambda x: None,
        lose_hook=lambda x: None):
            self.name = name
            self.get_hook = get_hook
            self.lose_hook = lose_hook

            if stacks:
                self.stacks = 1

        def get_hook(self):
            if self.stacks:
                self.stacks += 1
                self.get_hook()

class Stats(object):
    def __init__(self, arg, update_hook = lambda x: None):
        self.name = name
        self.value = value
        self.update_hook = update_hook

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, val):
        self.value = value
        self.update_hook(value)
