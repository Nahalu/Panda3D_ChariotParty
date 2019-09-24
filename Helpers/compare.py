def compare(players):

    n = len(players)
    for i in range(n):
        for j in range(0, n-i-1):
            # Swap if elem is greater than the next
            if players[j]["gold"] > players[j+1]["gold"]:
                players[j]["gold"], players[j +
                                            1]["gold"] = players[j+1]["gold"], players[j]["gold"]

            if players[j]["gold"] == players[j+1]["gold"]:
                players[j]["carbon"], players[j +
                                              1]["carbon"] = players[j+1]["carbon"], players[j]["carbon"]
