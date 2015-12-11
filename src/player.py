class Player:
    def __init__(self, name, items=None, stats=None):
        self.name = name
        if items is None:
            self.items = []

        if stats is None:
            self.stats = stats

    def get_item(item):
        self.items[item.type] += 1

    def lose_item(item):
        self.items[item.type] += 1

    def stat_check(self, stat_name, target, leq=False):
        stat = self.stats[stat_name]

        if not leq:
            return stat >= target
        else:
            return stat <= target

class Item(object):
    def __init__(self, arg):
        pass
        
class Stats(object):
    def __init__(self, arg):
        pass
