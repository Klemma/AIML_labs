def array_to_dict(array: list) -> dict:
    return {array[i]: [item[0] for item in list(enumerate(array)) if item[1] == array[i]] for i in range(len(array))}


def jaccard_similarity(set1: set, set2: set) -> float:
    intersec_size = 0
    union_size = len(set1) + len(set2)
    for item in set1:
        if item in set2:
            intersec_size += 1
        else:
            union_size -= 1
    return intersec_size / union_size


if __name__ == '__main__':
    print(array_to_dict(['a', 'b', 'c', 'd', 'e', 'a', 'a', 'b', 'c']))
    print("Метрика Жаккарда: " + str(jaccard_similarity({1, 2, 3}, {2, 4, 5})))
