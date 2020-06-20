import random

ALLOWED_EDGES = (4, 6, 8, 10, 12, 20)


def roll(dice):
    # This function generates random numbers in one of the allowed ranges.
    # It takes string in xdy format, where x is the quantity of rolls and y is the dice edges amount
    dice = dice.translate(str.maketrans({'x': 'd', 's': 'd', 'e': 'd', 'r': 'd', 'f': 'd', 'c': 'd'}))
    rolls_qnt, edges = dice.split('d')
    rolls_qnt, edges = int(rolls_qnt), int(edges)
    if edges not in ALLOWED_EDGES:
        return 'Ты инвалид, нет такого кубика'

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
    if int(dice.split('d')[0]) == 1:
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
    return random.randint(0, 1)


def death_roll():
    successes, failures = 0, 0

    while successes < 3 and failures < 3:
        if flip_coin():
            successes += 1
        else:
            failures += 1

        if successes == 3:
            return "Congratulations, you have survived"
        elif failures == 3:
            return "Sorry, but your character is dead"
