terminator = {'unit_name' = 'terminator', 'm': 5, 't': 5, 'sv':2, 'w':3, 'ld':6, 'oc':1 }
terminator_storm_bolter = {'r': 24, 'a': 2, 'bs': 3, 's':4, 'ap':0, 'd':1, 'abilities': 'rapid_fire'}
termaguant = {'unit_name': 'termaguant', 'm': 5, 't': 5, 'sv':2, 'w':3, 'ld':6, 'oc':1 }
termaguant_fleshborer = {'r': 18, 'a': 1, 'bs': 4, 's':5, 'ap':0, 'd':1}
print(terminator_storm_bolter)


import random

def shooting(weapon, target_unit, models=1, within_half_range=True):
    """
    Calculate the total damage dealt by a weapon with the Rapid Fire ability.

    :param weapon: dict, weapon stats (e.g., terminator_storm_bolter)
    :param target_unit: dict, target unit stats (e.g., termaguant)
    :param models: int, number of models firing the weapon
    :param within_half_range: bool, whether the target is within half range
    :return: dict, total damage dealt and remaining wounds of the target
    """
    #00 - TARGET DATA
    target_toughness = target_unit['t']  # Toughness
    target_save = target_unit['sv']  # Save value
    target_wounds = target_unit['w']  # Total wounds

    #01- ATTACK QTY
    base_attacks = weapon['a']
    if 'abilities' in weapon and 'rapid_fire' in weapon['abilities']:
        attacking_abilities = int(weapon['abilities'].split('_')[-1])
    else:
        attacking_abilities =1 
    
    total_attacks = base_attacks * attacking_abilities if within_half_range else base_attacks
    total_attacks *= models

    #02 - ATTACK ROLLS
    hits = 0
    for _ in range(total_attacks):
        if random.randint(1, 6) >= weapon['bs']:  # Hit on BS or better
            hits += 1

    #03 -  WOUNDS
    wounds = 0
    for _ in range(hits):
        if weapon['s'] >= 2 * target_toughness:  
            wound_roll = 2
        elif weapon['s'] > target_toughness:  
            wound_roll = 3
        elif weapon['s'] == target_toughness: 
            wound_roll = 4
        elif weapon['s'] < target_toughness:  
            wound_roll = 5
        else:  
            wound_roll = 6

        if random.randint(1, 6) >= wound_roll:  # Successful wounds
            wounds += 1

    #04 -SAVE THROW
    failed_saves = 0
    for _ in range(wounds):
        save_roll = target_save - weapon['ap']  # Wep AP Ability
        if random.randint(1, 6) < save_roll:
            failed_saves += 1

    #05 - DAMAGE DONE
    total_damage = failed_saves * weapon['d']

    #06 - UNIT WOUND REDUCTION
    remaining_wounds = max(0, target_wounds - total_damage)

    return {
        'total_damage': total_damage,
        'remaining_wounds': remaining_wounds
    }


shooting(termaguant_fleshborer, terminator, models=1, within_half_range=True)
    
