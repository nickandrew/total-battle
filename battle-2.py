#!/usr/bin/env python3
"""Simulate an algorithm stress-testing battle."""

from dataclasses import dataclass

import tb

my_army = tb.Army([
    tb.Squad(tb.catapult_4,  2200, 130.5, 105.0, 6.0),
    tb.Squad(tb.spearman_4, 13295, 455.0, 373.5, 8.6),
])

cursed_citadel_l20_2 = tb.Army([
    tb.Squad(tb.werewolf, 2900, 0, 0),
    tb.Squad(tb.death_rider, 650, 0, 0),
    tb.Squad(tb.giant_zombie, 80, 0, 0),
    tb.Squad(tb.bull_rider, 54, 0, 0),
    tb.Squad(tb.cursed_dragon, 10, 0, 0),
])

def main():
    enemy = cursed_citadel_l20_2

    print('\n'.join(my_army.report()))
    print('')
    print('\n'.join(enemy.report()))

    tb.fight_all(enemy, my_army)

if __name__ == '__main__':
    main()
