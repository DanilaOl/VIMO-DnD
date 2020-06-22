import functions as f
from math import floor


# class Character:
#     def __init__(self, character_name, strength, dexterity, constitution, intelligence, wisdom, charisma):
#         self.character_name = character_name
#         self.strength = strength
#         self.dexterity = dexterity
#         self.constitution = constitution
#         self.intelligence = intelligence
#         self.wisdom = wisdom
#         self.charisma = charisma
#         self.str_mod = floor((strength - 10)/2)
#         self.dex_mod = floor((dexterity - 10)/2)
#         self.cons_mod = floor((constitution - 10) / 2)
#         self.int_mod = floor((intelligence - 10) / 2)
#         self.wis_mod = floor((wisdom - 10) / 2)
#         self.char_mod = floor((charisma - 10) / 2)
#         self.initiative = self.dex_mod
#
#     def roll_initiative(self):
#         score = int(f.roll('1d20'))
#         output = f"{score} + {self.initiative} = {score + self.initiative}"
#         return output
#
# # TODO: Send all stats in PM and do not save into file. Hence, need to delete roll_initiative()
#
#
# me = Character('Дазваир', 14, 8, 15, 10, 16, 12)
#
# print(me.roll_initiative())

def create_character(name, race, ch_class, strength, dexterity, constitution, intelligence, wisdom, charisma):
    str_mod = floor((int(strength) - 10) / 2)
    dex_mod = floor((int(dexterity) - 10) / 2)
    cons_mod = floor((int(constitution) - 10) / 2)
    int_mod = floor((int(intelligence) - 10) / 2)
    wis_mod = floor((int(wisdom) - 10) / 2)
    char_mod = floor((int(charisma) - 10) / 2)
    output = f"Имя персонажа: {name}\n" \
             f"Раса: {race}\n" \
             f"Класс: {ch_class}\n" \
             f"Сила: {strength}({str_mod})\n" \
             f"Ловкость: {dexterity}({dex_mod})\n" \
             f"Телосложение: {constitution}({cons_mod})\n" \
             f"Интеллект: {intelligence}({int_mod})\n" \
             f"Мудрость: {wisdom}({wis_mod})\n" \
             f"Харизма: {charisma}({char_mod})\n" \
             f"Бонус инициативы: {dex_mod}"
    return output



