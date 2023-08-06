import sys

WEAPONS = [
    { 'name': 'Dagger'      , "cost":   8, "damage" :  4, "armor":  0 },
    { 'name': 'Shortsword'  , "cost":  10, "damage" :  5, "armor":  0 },
    { 'name': 'Warhammer'   , "cost":  25, "damage" :  6, "armor":  0 },
    { 'name': 'Longsword'   , "cost":  40, "damage" :  7, "armor":  0 },
    { 'name': 'Greataxe'    , "cost":  74, "damage" :  8, "armor":  0 },
]


ARMOR = [
    { 'name': 'None'        , 'cost':   0, 'damage':  0, 'armor':  0 },
    { 'name': 'Leather'     , 'cost':  13, 'damage':  0, 'armor':  1 },
    { 'name': 'Chainmail'   , 'cost':  31, 'damage':  0, 'armor':  2 },
    { 'name': 'Splintmail'  , 'cost':  53, 'damage':  0, 'armor':  3 },
    { 'name': 'Bandedmail'  , 'cost':  75, 'damage':  0, 'armor':  4 },
    { 'name': 'Platemail'   , 'cost': 102, 'damage':  0, 'armor':  5 },
]

RINGS = [
    { 'name': 'None'      , 'cost':   0, 'damage': 0, 'armor': 0 }
    { 'name': 'Damage +1' , 'cost':  25, 'damage': 1, 'armor': 0 },
    { 'name': 'Damage +2' , 'cost':  50, 'damage': 2, 'armor': 0 },
    { 'name': 'Damage +3' , 'cost': 100, 'damage': 3, 'armor': 0 },
    { 'name': 'Defense +1', 'cost':  20, 'damage': 0, 'armor': 1 },
    { 'name': 'Defense +2', 'cost':  40, 'damage': 0, 'armor': 2 },
    { 'name': 'Defense +3', 'cost':  80, 'damage': 0, 'armor': 3 },
]

class Player(object):

    def ___init__(self):
        self._hits = None
        self._armor = None
        self._damage = None

    def setup(self, hits, damage, armor):
        self._hits = hits
        self._damage = damage
        self._armor = armor

class Runner(object):

    def __init__(self, value):
        pass

    def initialize(self):

        print("initialize")

    def run(self):

        for weapon in WEAPONS:
            cost1 = weapon['cost']
            damage1 = weapon['damage']

            for armor in ARMOR:
                cost2 = armor['cost']
                damage2 = weapon['damage']

                for ring1 in RINGS:
                    cost3 = ring1['cost']
                    for ring2 in RINGS:
                        if ring1 == ring2:
                            continue

                        cost4 = ring2['cost']

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


