#!/usr/bin/env python3
"""Total Battle troop definitions and fight simulator."""

from dataclasses import dataclass
import copy

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
    training_cost: int = 0     # Silver cost
    killed: int = 0

    def __deepcopy__(self, memo):
        new = self.__class__(
            troop=self.troop,
            qty=self.qty,
            strength_bonus=self.strength_bonus,
            health_bonus=self.health_bonus,
            double_damage=self.double_damage,
        )

        memo[id(self)] = new
        return new

    def unit_health(self):
        """Calculate per-unit health, including bonuses."""
        return float(self.troop.health * (1 + self.health_bonus / 100.0))

    def unit_strength(self):
        """Calculate per-unit strength, including bonuses."""
        return float(self.troop.strength * (1 + self.strength_bonus / 100.0))

    def total_health(self):
        """Calculate total health, including bonuses."""
        th = self.qty * self.unit_health()
        print(f'   Total_health: {self.qty} {self.troop.health} {self.health_bonus} {self.unit_health()} {th}')
        return self.qty * self.unit_health()

    def total_strength(self):
        """Calculate total strength, including bonuses."""
        return float(self.qty * self.unit_strength())

    def damage_against(self, other_squad) -> int:
        """Calculate how much damage this Squad can do against another."""
        base_strength = self.total_strength()

        # Calculate strength bonus against various types of enemy
        # In case the enemy meets 2 or more of the bonus criteria, only the largest % applies
        augmented_strength = 1
        for s, v in self.troop.strengths.items():
            if s in other_squad.troop.features:
                a_s = (1 + v / 100.0)
                if a_s > augmented_strength:
                    augmented_strength = a_s

        tot_strength = float(base_strength * augmented_strength)
        tot_health = other_squad.total_health()
        print(f'    {self.troop.name:20} against {other_squad.troop.name:20} qty {other_squad.qty:8} str {base_strength} aug {augmented_strength:4.2f} tot {tot_strength:10.1f} health {tot_health:10.1f}')
        # The amount of damage we can do is limited by the total health of the enemy
        # return min(tot_strength, tot_health)
        return tot_strength

    def tie_breaker_3(self, attack_candidates):
        """Choose who gets attacked. It's mostly wrong.

        Pick the one that can retaliate hardest
        """

        tot_s = self.total_strength()
        max_thing = 0
        for squad in attack_candidates:
            tot_h = squad.total_health()
            could_kill = int(self.total_strength() / squad.unit_health())
            damage = squad.damage_against(self)
            killed_damage = damage * could_kill / squad.qty
            print(f'      --- {squad.troop.name} qty {could_kill:6} could do {damage:10.1f} -> {killed_damage:10.1f}')
            criteria = killed_damage
            print(f'      --- {squad.troop.name:20} score {criteria:10.1f}')
            if criteria > max_thing:
                max_thing = criteria
                to_attack = squad

        return to_attack

    def choose_attack(self, army):
        """Choose which squad in an enemy army to attack."""
        print(f'--- Choosing which squad {self.troop.name} (strength {self.total_strength()}) will attack')
        md = 0
        attack_candidates = list()

        for squad in army.squads:
            if squad.qty == 0:
                # Can't attack a squad that's already completely dead
                continue

            smd = min(squad.total_health(), self.damage_against(squad))
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
            tot_s = self.total_strength()
            print(f'    -- Tie breaker - total_strength {tot_s}')
            for squad in attack_candidates:
                tot_h = squad.total_health()
                could_kill = int(self.total_strength() / squad.unit_health())
                print(f'        -- Considering {squad.troop.name:20} qty {squad.qty:10} unit_s {squad.unit_strength():8.1f} health {squad.total_health():10.1f} could kill {could_kill:10}')

            to_attack = self.tie_breaker_3(attack_candidates)

            print(f'        -- Chose {to_attack.troop.name}')

        uh = to_attack.unit_health()
        kills = int(md / uh)
        print(f'   Damage: {md} against {to_attack.troop.name} kills {kills} {md / uh}')
        if kills > to_attack.qty:
            raise ValueError(f'Cannot kill {kills} which is more than {to_attack.qty}')
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
                print(f'    Skip {squad.troop.name:20} qty {squad.qty:8} (used)')
                continue
            ts = squad.total_strength()
            print(f'         {squad.troop.name:20} qty {squad.qty:8} total strength {ts:10.1f}')
            if ts > best_s:
                best_s = ts
                best = squad

        if best is None:
            return None

        print(f'    Best is {best.troop.name} qty {best.qty} total strength {best_s}')
        return best

    def new(self):
        return copy.deepcopy(self)

    def report(self) -> list:
        """Return a structured report of this army's composition."""
        ls = []

        for squad in self.squads:
            ls.append({
                'name': squad.troop.name,
                'qty': squad.qty,
                'tot_s': squad.total_strength(),
                'unit_s': squad.unit_strength(),
                'tot_h': squad.total_health(),
                'killed': squad.killed,
            })

        ret = []
        for d in sorted(ls, key=lambda x: -x['tot_h']):
            ret.append(f"{d['name']:20} qty {d['qty']:8} us {d['unit_s']:8.1f} s {d['tot_s']:10.1f} h {d['tot_h']:10.1f} killed {d['killed']}")
        return ret

    def alive_squads(self) -> int:
        """Return number of squads with live troops."""
        ret = 0
        for squad in self.squads:
            if squad.qty > 0:
                ret += 1

        return ret


citadel_walls = Troop('Citadel Walls', 10000, 30000, set(['fortification', 'engineer']), {'melee': 100, 'mounted': 100, 'ranged': 100})
cursed_dragon = Troop('Cursed Dragon', 320000, 960000, set(['flying', 'dragon', 'cursed']), {'giant': 50, 'mounted': 50})
giant_zombie = Troop('Giant Zombie', 33000, 99000, set(['melee', 'giant', 'cursed']), {'beast': 45, 'mounted': 70})
death_rider = Troop('Death Rider', 3200, 9600, set(['mounted', 'cursed']), {'ranged': 50})
bull_rider = Troop('Bull Rider', 29000, 87000, set(['mounted', 'cursed']), {'ranged': 55})
werewolf = Troop('Werewolf', 360, 1080, set(['melee', 'beast', 'cursed']), {'mounted': 45})

catapult_4 = Troop('Catapult IV', 1460, 8750, set(['siege', 'engineer', 'human']), {'fortification': 219})

spearman_4 = Troop('Spearman IV', 290, 870, set(['melee', 'guardsman', 'human']), {'beast': 270, 'mounted': 132})
spearman_3 = Troop('Spearman III', 160, 480, set(['melee', 'guardsman', 'human']), {'beast': 180, 'mounted': 88})
spearman_2 = Troop('Spearman II', 90, 270, set(['melee', 'guardsman', 'human']), {'beast': 120, 'mounted': 59})
spearman_1 = Troop('Spearman I', 50, 150, set(['melee', 'guardsman', 'human']), {'beast': 80, 'mounted': 39})

swordsman_3 = Troop('Swordsman III', 160, 480, set(['melee', 'specialist', 'human']), {'beast': 90, 'human': 105, 'mounted': 44})
swordsman_2 = Troop('Swordsman II', 90, 270, set(['melee', 'specialist', 'human']), {'beast': 60, 'human': 105, 'mounted': 29})
swordsman_1 = Troop('Swordsman I', 50, 150, set(['melee', 'specialist', 'human']), {'beast': 40, 'human': 105, 'mounted': 20})

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

def fight_round(army, enemy, army_allowed):
    if not army_allowed:
        # We've run out of attacking forces this phase
        return None, None, None, None

    strongest = army.choose_strongest(army_allowed)
    if not strongest:
        print(f'Nobody can fight')
        return None, None, None, None

    opponent, damage, kills = strongest.choose_attack(enemy)
    opponent.qty -= kills
    opponent.killed += kills
    print(f'{strongest.troop.name} attacks {opponent.troop.name} damage {damage} kills {kills} left {opponent.qty}')
    army_allowed.remove(strongest.troop.name)
    return strongest, opponent, damage, kills

def fight_all(my_army, enemy):
    """Fight the enemy until only one army remains.

    Enemy goes first.
    """

    # Enemy goes first
    army_1 = enemy
    army_2 = my_army

    # Set up a fresh attack phase
    army_1_allowed = None
    army_2_allowed = None

    while my_army.alive_squads() > 0 and enemy.alive_squads() > 0:
        if army_1_allowed:
            attacker, attacked, damage, kills = fight_round(army_1, army_2, army_1_allowed)
        elif army_2_allowed:
            print('Switch and continue')
            army_1, army_2 = army_2, army_1
            army_1_allowed, army_2_allowed = army_2_allowed, army_1_allowed
            continue
        else:
            # Refresh armies
            army_1_allowed = set(x.troop.name for x in army_1.squads if x.qty > 0)
            army_2_allowed = set(x.troop.name for x in army_2.squads if x.qty > 0)
            continue

        if attacker is None:
            # Could not find anybody to attack
            army_1_allowed = set()
        else:
            result = (attacker.troop.name, attacked.troop.name, damage, kills)
            # print(f'{result[0]} attacks {result[1]} damage {result[2]} kills {result[3]}')

        # Swap armies for next round
        army_1, army_2 = army_2, army_1
        army_1_allowed, army_2_allowed = army_2_allowed, army_1_allowed

    return army_1, army_2
