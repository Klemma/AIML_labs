def jaccard_similarity(set1: set, set2: set) -> float:
    intersec_size = 0
    union_size = len(set1) + len(set2)
    for item in set1:
        if item in set2:
            intersec_size += 1
            union_size -= 1

    return intersec_size / union_size


if __name__ == '__main__':
    print("Метрика Жаккарда: " + str(jaccard_similarity({1, 2, 3}, {2, 4, 5})))
