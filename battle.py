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
    enemy_allowed = set(x.troop.name for x in enemy.squads)
    myarmy_allowed = set(x.troop.name for x in my_army.squads)

    # Round 1 - Siege (not included here)

    # Round 2
    strongest = enemy.choose_strongest(enemy_allowed)
    opponent, damage, kills = strongest.choose_attack(my_army)
    print(f'{strongest.troop.name} attacks {opponent.troop.name} damage {damage} kills {kills}')
    opponent.qty -= kills
    enemy_allowed.remove(strongest.troop.name)
    print('')

    # Round 3
    strongest = my_army.choose_strongest(myarmy_allowed)
    opponent, damage, kills = strongest.choose_attack(enemy)
    print(f'{strongest.troop.name} attacks {opponent.troop.name} damage {damage} kills {kills}')
    opponent.qty -= kills
    myarmy_allowed.remove(strongest.troop.name)
    print('')

    # Round 4
    strongest = enemy.choose_strongest(enemy_allowed)
    opponent, damage, kills = strongest.choose_attack(my_army)
    print(f'{strongest.troop.name} attacks {opponent.troop.name} damage {damage} kills {kills}')
    opponent.qty -= kills
    enemy_allowed.remove(strongest.troop.name)
    print('')

    # Round 5
    strongest = my_army.choose_strongest(myarmy_allowed)
    opponent, damage, kills = strongest.choose_attack(enemy)
    print(f'{strongest.troop.name} attacks {opponent.troop.name} damage {damage} kills {kills}')
    opponent.qty -= kills
    myarmy_allowed.remove(strongest.troop.name)
    print('')

    # Round 6
    strongest = enemy.choose_strongest(enemy_allowed)
    opponent, damage, kills = strongest.choose_attack(my_army)
    print(f'{strongest.troop.name} attacks {opponent.troop.name} damage {damage} kills {kills}')
    opponent.qty -= kills
    enemy_allowed.remove(strongest.troop.name)
    print('')

    # Round 7
    strongest = my_army.choose_strongest(myarmy_allowed)
    opponent, damage, kills = strongest.choose_attack(enemy)
    print(f'{strongest.troop.name} attacks {opponent.troop.name} damage {damage} kills {kills}')
    opponent.qty -= kills
    myarmy_allowed.remove(strongest.troop.name)
    print('')

    # Round 8
    strongest = enemy.choose_strongest(enemy_allowed)
    opponent, damage, kills = strongest.choose_attack(my_army)
    print(f'{strongest.troop.name} attacks {opponent.troop.name} damage {damage} kills {kills}')
    opponent.qty -= kills
    enemy_allowed.remove(strongest.troop.name)
    print('')

    # Round 9
    strongest = my_army.choose_strongest(myarmy_allowed)
    opponent, damage, kills = strongest.choose_attack(enemy)
    print(f'{strongest.troop.name} attacks {opponent.troop.name} damage {damage} kills {kills}')
    opponent.qty -= kills
    myarmy_allowed.remove(strongest.troop.name)
    print('')

    # Round 10
    strongest = enemy.choose_strongest(enemy_allowed)
    opponent, damage, kills = strongest.choose_attack(my_army)
    print(f'{strongest.troop.name} attacks {opponent.troop.name} damage {damage} kills {kills}')
    opponent.qty -= kills
    enemy_allowed.remove(strongest.troop.name)
    print('')

    # Round 11
    strongest = my_army.choose_strongest(myarmy_allowed)
    opponent, damage, kills = strongest.choose_attack(enemy)
    print(f'{strongest.troop.name} attacks {opponent.troop.name} damage {damage} kills {kills}')
    opponent.qty -= kills
    myarmy_allowed.remove(strongest.troop.name)
    print('')


if __name__ == '__main__':
    main()
