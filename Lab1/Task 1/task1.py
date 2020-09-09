def array_to_dict(array: list) -> dict:
    return {array[i]: [item[0] for item in list(enumerate(array)) if item[1] == array[i]] for i in range(len(array))}


if __name__ == '__main__':
    print(array_to_dict(['a', 'b', 'c', 'd', 'e', 'a', 'a', 'b', 'c']))
