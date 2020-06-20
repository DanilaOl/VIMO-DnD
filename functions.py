import random

ALLOWED_EDGES = (4, 6, 8, 10, 12, 20)


def roll(dice):
    # This function generates random numbers in one of allowed ranges.
    # It takes string in xdy format, where x is quantity of rolls and y is dice edges amount
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
    # Makes 2 rolls and choosing greatest
    rolls = [roll(dice), roll(dice)]
    output = " или ".join(rolls) + f". Итого {max(rolls)}"
    return output


def disadvantage_roll(dice):
    # Makes 2 rolls and choosing lowest
    rolls = [roll(dice), roll(dice)]
    output = " или ".join(rolls) + f". Итого {min(rolls)}"
    return output
