def tri_bulle(players):

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


tab = [{"gold": 5, "carbon": 1}, {"gold": 1,
                                  "carbon": 10}, {"gold": 1, "carbon": 11}]
tri_bulle(tab)
print("Le tableau trié est:")
for i in range(len(tab)):
    print(tab[i])
