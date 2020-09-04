import requests


def get_txt_from_url(url: str) -> str:
    return requests.get(url).text


def get_users_set(txt: str) -> set:
    return set(txt.split())


def get_friends_relations(txt: str) -> dict:
    txt_splitted = txt.split()
    friends_relations = dict()

    for item in txt_splitted:
        friends_relations[item] = 1 if item not in friends_relations else friends_relations[item] + 1

    return friends_relations


if __name__ == '__main__':
    txt = get_txt_from_url("https://raw.githubusercontent.com/Klemma/AIML_labs/master/arcs_refined.txt")
    users = get_users_set(txt)
    print("Количество уникальных пользователей равно " + str(len(users)))

    friends_relations = sorted(get_friends_relations(txt).items(), key=lambda x: x[1], reverse=True)
    print("\nТоп 15 пользователей по количеству друзей:")
    for i in range(15):
        print(friends_relations[i])

