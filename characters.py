import json
from math import floor
from exceptions import WrongCharacterRace, WrongCharacterClass

race_features = json.load(open('race_features.json', 'r', encoding='utf-8'))
class_features = json.load(open('class_features.json', 'r', encoding='utf-8'))


def create_character(name, race, ch_class, strength, dexterity, constitution, intelligence, wisdom, charisma):
    # Creates character using your stats
    strength = int(strength)
    dexterity = int(dexterity)
    constitution = int(constitution)
    intelligence = int(intelligence)
    wisdom = int(wisdom)
    charisma = int(charisma)

    strength, dexterity, constitution, intelligence, wisdom, charisma = \
        apply_race_bonuses(race, strength, dexterity, constitution, intelligence, wisdom, charisma)

    strength, dexterity, constitution, intelligence, wisdom, charisma = \
        apply_class_bonuses(ch_class, strength, dexterity, constitution, intelligence, wisdom, charisma)

    str_mod, dex_mod, cons_mod, int_mod, wis_mod, char_mod = \
        calc_modifiers(strength, dexterity, constitution, intelligence, wisdom, charisma)

    hit_points = calc_hit_points(ch_class, cons_mod)

    output = f"Имя персонажа: {name}\n" \
             f"Раса: {race}\n" \
             f"Класс: {ch_class}\n" \
             f"Сила: {strength}({str_mod})\n" \
             f"Ловкость: {dexterity}({dex_mod})\n" \
             f"Телосложение: {constitution}({cons_mod})\n" \
             f"Интеллект: {intelligence}({int_mod})\n" \
             f"Мудрость: {wisdom}({wis_mod})\n" \
             f"Харизма: {charisma}({char_mod})\n" \
             f"Бонус инициативы: {dex_mod}\n" \
             f"Кость хитов: {class_features[ch_class]['hit_dice']}\n" \
             f"Максимум хитов: {hit_points}"
    return output


def apply_race_bonuses(race, strength, dexterity, constitution, intelligence, wisdom, charisma):
    # Function that applies race bonuses to the stats
    try:
        strength += int(race_features[race]['str_bonus'])
        dexterity += race_features[race]['dex_bonus']
        constitution += race_features[race]['cons_bonus']
        intelligence += race_features[race]['int_bonus']
        wisdom += race_features[race]['wis_bonus']
        charisma += race_features[race]['char_bonus']
    except KeyError:
        raise WrongCharacterRace
    else:
        return strength, dexterity, constitution, intelligence, wisdom, charisma


def apply_class_bonuses(ch_class, strength, dexterity, constitution, intelligence, wisdom, charisma):
    # Function that applies race bonuses to the stats
    try:
        strength += class_features[ch_class]['str_bonus']
        dexterity += class_features[ch_class]['dex_bonus']
        constitution += class_features[ch_class]['cons_bonus']
        intelligence += class_features[ch_class]['int_bonus']
        wisdom += class_features[ch_class]['wis_bonus']
        charisma += class_features[ch_class]['char_bonus']
    except KeyError:
        raise WrongCharacterClass
    return strength, dexterity, constitution, intelligence, wisdom, charisma


def calc_modifiers(strength, dexterity, constitution, intelligence, wisdom, charisma):
    # Calculates modifiers for the stats
    str_mod = floor((int(strength) - 10) / 2)
    dex_mod = floor((int(dexterity) - 10) / 2)
    cons_mod = floor((int(constitution) - 10) / 2)
    int_mod = floor((int(intelligence) - 10) / 2)
    wis_mod = floor((int(wisdom) - 10) / 2)
    char_mod = floor((int(charisma) - 10) / 2)
    return str_mod, dex_mod, cons_mod, int_mod, wis_mod, char_mod


def calc_hit_points(ch_class, cons_mod):
    # Calculates maximum hit points for the character
    hit_points = int(class_features[ch_class]['hit_dice'][2:]) + cons_mod
    return hit_points
