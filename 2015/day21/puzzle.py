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
    { 'name': 'None'      , 'cost':   0, 'damage': 0, 'armor': 0 },
    { 'name': 'Damage +1' , 'cost':  25, 'damage': 1, 'armor': 0 },
    { 'name': 'Damage +2' , 'cost':  50, 'damage': 2, 'armor': 0 },
    { 'name': 'Damage +3' , 'cost': 100, 'damage': 3, 'armor': 0 },
    { 'name': 'Defense +1', 'cost':  20, 'damage': 0, 'armor': 1 },
    { 'name': 'Defense +2', 'cost':  40, 'damage': 0, 'armor': 2 },
    { 'name': 'Defense +3', 'cost':  80, 'damage': 0, 'armor': 3 },
]

class ExcpetionLost(Exception):
    pass

class Player(object):

    def ___init__(self, name):
        self._name = name
        self._hits = None
        self._armor = None
        self._damage = None

    def setup(self, hits, damage, armor):
        self._hits = hits
        self._damage = damage
        self._armor = armor

    def get_damage(self):
        return self._damage

    def get_armor(self):
        return self._armor

    def take_hits(self, hits):
        self._hits -= hits
        if self._hits <= 0:
            raise ExcpetionLost("%s lost" % self._name)

class Runner(object):

    def __init__(self, value):
        self._game_count = 0
        self._min_cost = 99999999999999

    def initialize(self):

        print("initialize")

    def play(self, player1, player2):

        while True:
            try:
            hits = player2.get_damage() - player2.get_armor()
            player2.take_hits(hits)


    def run(self):

        for weapon in WEAPONS:
            cost1 = weapon['cost']
            damage1 = weapon['damage']
            armor1 = weapon['armor']

            for armor in ARMOR:
                cost2 = armor['cost']
                damage2 = armor['damage']
                armor2 = armor['armor']

                for ring1 in RINGS:
                    cost3 = ring1['cost']
                    damage3 = ring1['damage']
                    armor3 = ring1['armor']

                    for ring2 in RINGS:
                        if ring1 == ring2:
                            continue

                    cost4 = ring2['cost']
                    damage4 = ring2['damage']
                    armor4 = ring2['armor']

                    total_cost = cost1 + cost2 + cost3 + cost4
                    total_damage = damage1 + damage2 + damage3 + damage4
                    total_armor = armor1 + armor2 + armor3 + armor4

                    print("Cost: %d damage: %d armor: %d" % (total_cost, total_damage, total_armor))

                    player1 = Player("me")
                    player1.setup(100, total_damage, total_armor)

                    player2 = Player("boss")
                    player2.setup(100, 8, 2)

                    self._play(player1, player2)
if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


