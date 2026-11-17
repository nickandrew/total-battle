#!/usr/bin/env python3
"""Test a battle against an L20 Cursed Citadel."""

from dataclasses import dataclass
import unittest

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

expected_results = [
    ('Cursed Dragon', 'Ettin', 4800000.0, 10),
    ('Spearman III', 'Cursed Dragon', 9600000.0, 10),
    ('Giant Zombie', 'Fearsome Manticore', 3828000.0, 8),
    ('Spearman IV', 'Giant Zombie', 7920000.0, 80),
    ('Death Rider', 'Spearman III', 2080000.0, 649),
    ('Catapult IV', 'Death Rider', 6240000.0, 650),
    ('Bull Rider', 'Spearman III', 1566000.0, 489),
    ('Fearsome Manticore', 'Bull Rider', 4698000.0, 54),
    ('Werewolf', 'Spearman IV', 1044000.0, 179),
    ('Ice Phoenix', 'Werewolf', 3132000.0, 2900),
]

class Fight(unittest.TestCase):
    def test_rounds(self):
        enemy = tb.cursed_citadel_l20.new()
        enemy_allowed = set(x.troop.name for x in enemy.squads)
        myarmy_allowed = set(x.troop.name for x in my_army.squads)

        # Print army make-up
        print('My army:')
        print('\n'.join(my_army.report()), '\n')
        print('Citadel army:')
        print('\n'.join(enemy.report()), '\n')

        # Enemy goes first
        army_1 = enemy
        army_1_allowed = enemy_allowed
        army_2 = my_army
        army_2_allowed = myarmy_allowed
        round = 0

        for expected in expected_results:
            round += 1
            print('\n\n' + '=' * 70)
            print('=' * 30, f'Round {round:2}', '=' * 30)
            print('')
            print('=== Attacker', '=' * 57)
            print('\n'.join(army_1.report()), '\n')
            print('=== Versus  ', '=' * 57)
            print('\n'.join(army_2.report()), '\n')

            attacker, attacked, damage, kills = tb.fight_round(army_1, army_2, army_1_allowed)
            result = (attacker.troop.name, attacked.troop.name, damage, kills)
            with self.subTest(expected=expected):
                if result == expected:
                    print(f'Pass! {result}')
                else:
                    print(f'** Fail! {result} expected {expected}')

                # self.assertEqual(result, expected)

            # Swap armies for next round
            army_1, army_2 = army_2, army_1
            army_1_allowed, army_2_allowed = army_2_allowed, army_1_allowed
