import copy
import sys

SPELLS = {
    'missle'    : {'cost':  53, 'damage': 4, 'effect':0, 'mana':   0, 'armor' : 0},
    'drain'     : {'cost':  73, 'damage': 2, 'effect':0, 'mana':   0, 'armor' : 0},
    'shield'    : {'cost': 113, 'damage': 0, 'effect':6, 'mana':   0, 'armor' : 7},
    'poison'    : {'cost': 173, 'damage': 3, 'effect':6, 'mana':   0, 'armor' : 0},
    'recharge'  : {'cost': 229, 'damage': 0, 'effect':5, 'mana': 101, 'armor' : 0},
}

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
        self._total_wins = 0
        self._total_losses = 0
        self._min_spent = None

    def initialize(self):

        print("initialize")

    def hit_boss(self, boss_hits, hits, spent):
        boss_hits -= hits
        if boss_hits <= 0:
            self._total_wins += 1
            if self._min_spent is None or spent < self._min_spent:
                self._min_spent = spent

        return boss_hits

    def play(self, state):

        mana = state['mana']
        spell = state['spell']
        round = state['round']
        hits = state['hits']
        boss_hits = state['boss_hits']
        spent = state['spent']

        timer_shield    = state['timer_shield']
        timer_poison    = state['timer_poison']
        timer_recharge  = state['timer_recharge']

#        print("round: %d wins: %d losses: %d min_spend: %s mana: %d hits: %d boss_hits: %d spell: %s" %
#              (round, self._total_wins, self._total_losses, repr(self._min_spent), mana, hits, boss_hits, repr(spell)))

        if round == 1:
            print("ROUND 1 spell: %s" % spell)

#            input("round: %d continue..." % round)

        # Spell is None on the first round, this kicks things off
        if spell is not None:


            # # Part 2. At the start of the player turn, lose 1 hit point
            hits -= 1
            if hits <= 0:
                # print("lost on part 2 hit")
                self._total_losses += 1
                return

            # First, are there any timers in effect?
            if timer_shield > 0:
                timer_shield -= 1

            if timer_poison > 0:
                # If this active it deals 3 damage
                boss_hits = self.hit_boss(boss_hits, 3, spent)
                if boss_hits <= 0:
                    print("win 1")
                    return
                timer_poison -= 1

            if timer_recharge > 0:
                mana += 101
                timer_recharge -= 1

            # Select a spell (was pre-chosen in the ?
            spell_meta = SPELLS[spell]
            cost = spell_meta['cost']

            # First, can I afford this spell?
            # If not, this branch is a dead end
            if mana - cost < 0:
                # print("cannot afford spell: %s" % spell)
                return

            spent += cost
            mana -= cost

            # Check the spells
            if self._min_spent is not None:
                if spent >= self._min_spent:
                    # This branch is a dead end
                    return

            if spell == 'missle':
                # This spell immediately does 4 hits damage
                boss_hits = self.hit_boss(boss_hits, 4, spent)
                if boss_hits <= 0:
                    print("win 2")
                    return

            elif spell == 'drain':
                # This spell immediately does 2 hits damage

                boss_hits = self.hit_boss(boss_hits, 2, spent)
                if boss_hits <= 0:
                    print("win 3")
                    return

                # Immediately adds 2 hits
                hits += 2

            elif spell == 'shield':
                if timer_shield > 0:
                    # Cannot cast this spell while in effect - branch a dead end
                    return
                timer_shield = 6

            elif spell == 'poison':
                if timer_poison > 0:
                    # Cannot cast this spell while in effect - branch a dead end
                    return
                timer_poison = 6

            elif spell == 'recharge':
                if timer_recharge > 0:
                    # Cannot cast this spell while in effect - branch a dead end
                    return
                timer_recharge = 5

            else:
                raise ValueError("not handled!!")

            # Now boss plays.  A spell cast in the players round will
            # take effect here if it persists

            # hits -= 1
            # if hits <= 0:
            #     self._total_losses += 1
            #     return

            if timer_poison > 0:
                # If this active it deals 3 damage
                boss_hits = self.hit_boss(boss_hits, 3, spent)
                if boss_hits <= 0:
                    print("win 4")
                    return

                timer_poison -= 1

            if timer_recharge > 0:
                mana += 101
                timer_recharge -= 1

            if timer_shield > 0:
                # My armor is 7 so boss only does two hits of damage
                hits -= 2
                timer_shield -= 1
            else:
                # No shield, boss does 9 hits
                # of damage
                hits -= 9

            if hits <= 0:
                self._total_losses += 1
                return

        round += 1


        # Part 2. At the start of the player turn, lose 1 hit point
        hits -= 0
        if hits <= 0:
            self._total_losses += 1
            return

        # Update game state for the next round
        state['spent'] = spent
        state['hits'] = hits
        state['boss_hits'] = boss_hits
        state['mana'] = mana
        state['timer_shield']   = timer_shield
        state['timer_poison']   = timer_poison
        state['timer_recharge'] = timer_recharge
        state['round'] = round

        # Recurse into next round ... play all possible spells
        for spell in SPELLS.keys():
            state_copy = copy.deepcopy(state)
            state_copy['spell'] = spell
            self.play(state_copy)


    def run(self):

        state = {
            'spent'         : 0,
            'mana'          : 500,
            'spell'         : None,
            'hits'          : 50,
            'round'         : 0,
            'boss_hits'     : 51,
            'boss_damage'   : 9,
            'timer_shield'  : 0,
            'timer_poison'  : 0,
            'timer_recharge': 0,

        }

        self.play(state)

        print("total wins: %d" % self._total_wins)
        print("min spent: %d" % self._min_spent)

if __name__ == '__main__':

    runner = Runner(sys.argv[1])
    runner.run()


