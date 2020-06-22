import os
import random

ALLOWED_EDGES = (4, 6, 8, 10, 12, 20)


def roll(dice):
    # This function generates random numbers in one of the allowed ranges.
    # It takes string in xdy or dy format, where x is the quantity of rolls and y is the dice edges amount
    dice = dice.translate(str.maketrans({'x': 'd', 's': 'd', 'e': 'd', 'r': 'd', 'f': 'd', 'c': 'd'}))
    rolls_qnt, edges = dice.split('d')
    if rolls_qnt == '':
        rolls_qnt = '1'
    rolls_qnt, edges = int(rolls_qnt), int(edges)
    if edges not in ALLOWED_EDGES:
        return 'Нет кубика с такими гранями'

    elif rolls_qnt == 1:
        score = random.randint(1, edges)
        return str(score)

    elif rolls_qnt > 1:
        all_scores = []

        while rolls_qnt >= 1:
            semi_score = random.randint(1, edges)
            all_scores.append(semi_score)
            rolls_qnt -= 1

        final_score = sum(all_scores)
        return all_scores, final_score


def show_score(dice):
    # Prettifying output of roll function
    if dice[0] == '1' or 'd':
        return roll(dice)
    else:
        all_scores, final_score = roll(dice)
        output = ' + '.join(str(i) for i in all_scores) + ' = ' + str(final_score)
        return output


def rand_params():
    # Generates random parameters for your character's stats
    params = []
    for i in range(6):
        scores = sorted(roll("4d6")[0])[1:]
        params.append(sum(scores))
    return str(params)


def advantage_roll(dice):
    # Makes 2 rolls and choosing the greatest
    rolls = [int(roll(dice)), int(roll(dice))]
    output = " или ".join(str(x) for x in rolls) + f". Итого {max(rolls)}"
    return output


def disadvantage_roll(dice):
    # Makes 2 rolls and choosing the lowest
    rolls = [int(roll(dice)), int(roll(dice))]
    output = " или ".join(str(x) for x in rolls) + f". Итого {min(rolls)}"
    return output


def flip_coin():
    # Simulates coin flipping
    coin = ('Орёл', 'Решка')
    return random.choice(coin)


def sum_files():
    # Counts the number of files in working directory
    file_count = next(os.walk(os.getcwd()))[2]
    return len(file_count)
