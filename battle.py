#!/usr/bin/env python3
"""Total Battle Fight simulator."""

from dataclasses import dataclass

import tb

my_army = tb.Army([
    tb.Squad(tb.catapult_4, 1400, 423.5, 385.5, 7.3),
    tb.Squad(tb.spearman_4, 7500, 534.5, 567, 8.9),
    tb.Squad(tb.spearman_3, 15595, 534.5, 567, 8.9),
    tb.Squad(tb.swordsman_3, 100, 258.5, 202),
    tb.Squad(tb.ettin, 33, 321.5, 222.5, 3),
    tb.Squad(tb.fearsome_manticore, 43, 281, 226.5, 3),
    tb.Squad(tb.ice_phoenix, 89, 277.5, 226.5, 3),
])

def main():
    enemy = tb.cursed_citadel_l20.new()

    print('\n'.join(my_army.report()))
    print('')
    print('\n'.join(enemy.report()))

    tb.fight_all(my_army, enemy)

if __name__ == '__main__':
    main()
