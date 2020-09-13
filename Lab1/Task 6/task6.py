import requests
import numpy as np
from scipy.sparse.csgraph import dijkstra


def get_txt_from_url(url: str) -> str:
    return requests.get(url).text


def get_users_set(txt: str) -> set:
    return set(txt.split())


def get_users_friends_amount(txt: str) -> dict:
    txt_splitted = txt.split()
    users_friends_amount = dict()

    for item in txt_splitted:
        users_friends_amount[item] = 1 if item not in users_friends_amount else users_friends_amount[item] + 1

    return users_friends_amount


def get_users_proportions(txt: str) -> dict:
    users = get_users_set(txt)
    users_enum = {val: key for key, val in dict(enumerate(users)).items()}

    users_pairs = [(users_enum[pair[0]], users_enum[pair[1]])
                   for pair in [pair.split(' ') for pair in txt.split('\n')]]

    adjacency_matrix = np.zeros((len(users), len(users)))
    for i in range(len(users_pairs)):
        user1 = users_pairs[i][0]
        user2 = users_pairs[i][1]
        adjacency_matrix[user1][user2] = 1
        adjacency_matrix[user2][user1] = 1

    dist_matrix = dijkstra(adjacency_matrix, directed=False)
    max_len = int(np.unique(dist_matrix)[-2])

    cartesian_product = [(user1, user2) for user1 in users for user2 in users if user1 != user2]

    def proportion(length: int) -> float:
        return np.count_nonzero(dist_matrix == length) / len(cartesian_product)

    proportions = {length: proportion(length) for length in range(1, max_len + 1)}
    proportions[np.inf] = proportion(np.inf)

    return proportions


def main():
    txt = get_txt_from_url("https://raw.githubusercontent.com/Klemma/AIML_labs/master/Lab1/Task%206/arcs_refined.txt")
    users = get_users_set(txt)
    print(f"Количество уникальных пользователей равно {len(users)}")

    users_friends_amount = sorted(get_users_friends_amount(txt).items(), key=lambda x: x[1], reverse=True)
    print("\nТоп 15 пользователей по количеству друзей:")
    for i in range(15):
        print(users_friends_amount[i])

    proportions = get_users_proportions(txt)
    print("\nПолученные пропорции пар пользователей:")
    for length, proportion in proportions.items():
        print(f"{length}: {proportion}")

    print(f"\nСумма полученных пропорций: {sum(proportions.values())}")


if __name__ == '__main__':
    main()
