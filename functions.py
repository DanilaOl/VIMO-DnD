import random
ALLOWED_EDGES = (4, 6, 8, 10, 12, 20)


def roll(dice):
    rolls_qnt, edges = dice.split('d')
    rolls_qnt, edges = int(rolls_qnt), int(edges)

    if rolls_qnt not in ALLOWED_EDGES:
        return 'Ty Invalid, Net Takogo Kubika'

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
        final_str = ' + '.join(str(i) for i in all_scores) + ' = ' + str(final_score)
        return final_str
