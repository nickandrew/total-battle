#!/usr/bin/env python3
"""Total Battle Fight simulator."""

from dataclasses import dataclass


@dataclass
class Troop:
    name: str
    strength: int
    health: int
    features: set = None     # Inherent nature of this type
    strengths: dict = None    # What this type is good at attacking

@dataclass
class Squad:
    troop: Troop
    qty: int
    strength_bonus: float
    health_bonus: float
    double_damage: float = 0

    def aug_strength(self):
        """Calculate strength including bonus."""
        return float(self.qty * self.troop.strength * (1 + self.strength_bonus / 100.0))

    def unit_health(self):
        """Calculate per-unit health, including bonuses."""
        return float(self.troop.health * (1 + self.health_bonus / 100.0))

    def total_health(self):
        """Calculate total health, including bonuses."""
        return self.qty * self.unit_health()

    def total_strength(self):
        """Calculate total strength, including bonuses."""
        return float(self.qty * self.troop.strength * (1 + self.strength_bonus / 100.0))

    def damage_against(self, other_squad) -> int:
        """Calculate how much damage this Squad can do against another."""
        base_strength = float(self.qty * self.troop.strength * (1 + self.strength_bonus / 100.0))
        augmented_strength = 1
        for s, v in self.troop.strengths.items():
            if s in other_squad.troop.features:
                a_s = (1 + v / 100.0)
                if a_s > augmented_strength:
                    augmented_strength = a_s

        tot_strength = float(base_strength * augmented_strength)
        print(f'    {self.troop.name} against {other_squad.troop.name} s {base_strength} as {augmented_strength} tot {tot_strength}')
        tot_health = other_squad.total_health()
        print(f'    Total health {tot_health}')
        return min(tot_strength, tot_health)

    def choose_attack(self, army):
        """Choose which squad in an enemy army to attack."""
        print(f'--- Choosing which squad {self.troop.name} (strength {self.aug_strength()}) will attack')
        md = 0
        attack_candidates = list()

        for squad in army.squads:
            smd = self.damage_against(squad)
            print(f'    Damage against {squad.troop.name} will be {smd}')
            if smd > md:
                md = smd
                attack_candidates = [squad]
            elif smd == md:
                attack_candidates.append(squad)

        if not attack_candidates:
            return None

        to_attack = attack_candidates[0]

        if len(attack_candidates) > 1:
            print(f'    -- Tie breaker')
            max_size = 0
            for squad in attack_candidates:
                could_kill = int(self.total_strength() / squad.unit_health())
                print(f'        -- tot_strength {self.total_strength()} enemy tot_health {squad.total_health()}')
                print(f'        -- Considering {squad.troop.name} size {squad.qty} health {squad.total_health()} could kill {could_kill}')
                if squad.qty > max_size:
                    max_size = squad.qty
                    to_attack = squad

            print(f'    -- Chose {to_attack.troop.name} because {to_attack.qty}')

        # smd = self.damage_against(to_attack)
        uh = to_attack.unit_health()
        kills = int(md / uh)
        print(f'   Damage: {md} against {to_attack.troop.name} kills {kills}')
        return to_attack, md, kills

@dataclass
class Army:
    squads: list[Squad]

    def choose_strongest(self, allowed_set):
        """Choose the strongest squad to use in an attack."""
        print(f'--- Choosing strongest squad')
        best = None
        best_s = 0
        for squad in self.squads:
            if squad.troop.name not in allowed_set:
                print(f'    Skipping {squad.troop.name} as already used this phase')
                continue
            ts = squad.total_strength()
            print(f'    {squad.troop.name} total strength {ts}')
            if ts > best_s:
                best_s = ts
                best = squad

        print(f'    Best is {best.troop.name} total strength {best_s}')
        return best


cursed_dragon = Troop('Cursed Dragon', 320000, 960000, set(['flying', 'dragon', 'cursed']), {'giant': 50, 'mounted': 50})
giant_zombie = Troop('Giant Zombie', 33000, 99000, set(['melee', 'giant', 'cursed']), {'beast': 45, 'mounted': 70})
death_rider = Troop('Death Rider', 3200, 9600, set(['mounted', 'cursed']), {'ranged': 50})
bull_rider = Troop('Bull Rider', 29000, 87000, set(['mounted', 'cursed']), {'ranged': 55})
werewolf = Troop('Werewolf', 360, 1080, set(['melee', 'beast', 'cursed']), {'mounted': 45})

catapult_4 = Troop('Catapult IV', 1460, 8750, set(['siege', 'engineer', 'human']), {'fortification': 219})
spearman_4 = Troop('Spearman IV', 290, 870, set(['melee', 'guardsman', 'human']), {'beast': 270, 'mounted': 132})
spearman_3 = Troop('Spearman III', 160, 480, set(['melee', 'guardsman', 'human']), {'beast': 180, 'mounted': 88})
swordsman_3 = Troop('Swordsman III', 160, 480, set(['melee', 'specialist', 'human']), {'beast': 90, 'human': 105, 'mounted': 44})
ettin = Troop('Ettin', 48000, 144000, set(['melee', 'giant']), {'fortification': 243, 'mounted': 334})
fearsome_manticore = Troop('Fearsome Manticore', 46000, 138000, set(['flying', 'beast']), {'flying': 253, 'giant': 324})
ice_phoenix = Troop('Ice Phoenix', 17000, 51000, set(['flying', 'elemental']), {'dragon': 162, 'flying': 223})

cursed_citadel_l20 = Army([
    Squad(werewolf, 2900, 0, 0),
    Squad(death_rider, 650, 0, 0),
    Squad(giant_zombie, 80, 0, 0),
    Squad(bull_rider, 54, 0, 0),
    Squad(cursed_dragon, 10, 0, 0),
])

my_army = Army([
    Squad(catapult_4, 1400, 423.5, 385.5, 7.3),
    Squad(spearman_4, 7500, 534.5, 567, 8.9),
    Squad(spearman_3, 15595, 534.5, 567, 8.9),
    Squad(swordsman_3, 100, 258.5, 202),
    Squad(ettin, 33, 321.5, 222.5, 3),
    Squad(fearsome_manticore, 43, 281, 226.5, 3),
    Squad(ice_phoenix, 89, 277.5, 226.5, 3),
])

def main():
    enemy = cursed_citadel_l20
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


if __name__ == '__main__':
    main()
