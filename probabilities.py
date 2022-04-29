import scipy.stats as st
import numpy as np
import matplotlib.pyplot as plt


def expValue(players, pack):

    # return average times num_players in pack
    total_val = 0
    for name in players:
        total_val += players[name].price

    avg_val = total_val / len(players)
    xVal = avg_val * pack
    return xVal


def calc_probs(players, pack):
    # assuming only gold players matter for now
    gold_rare = pack["gold_rare"]

    # hypergeom inputs
    num_players = len(players)
    winners = 23  # ex. tots available

    dist = st.hypergeom(num_players, winners, gold_rare)

    x = np.arange(0, winners + 1)
    probs = dist.pmf(x)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, probs, 'bo')
    ax.vlines(x, 0, probs, lw=2)
    ax.set_xlabel('# of tots')
    ax.set_ylabel('hypergeom PMF')
    # plt.show()

    xTots = 0
    for i in range(len(probs)):
        xTots += i * probs[i]

    print(xTots)


# 143 for 84+
# 98 for 85+
# 23 for tots
available = 143 + 23

players = [i + 1 for i in range(available)]

pack = {"gold_rare": 25, "gold_nonrare": 0}
