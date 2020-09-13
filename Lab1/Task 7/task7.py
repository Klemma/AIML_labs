from string import digits, punctuation


def prepare_text(text: str) -> str:
    text = text.lower().replace('\n', ' ')
    text = text.translate(str.maketrans('', '', digits))
    text = text.translate(str.maketrans('', '', punctuation))
    return text


def get_chars_combinations(text: str, comb_len: int) -> dict:
    combinations = {}
    comb = ""
    for ch in text:
        if ch != ' ':
            comb += ch
        else:
            comb = ""
            continue
        if len(comb) == comb_len:
            combinations[comb] = 1 if comb not in combinations else combinations[comb] + 1
            comb = comb[1:]
    return combinations


def determine_text_language(text: str, similar_combs: dict, ru_ch_combs, bg_ch_combs) -> dict:
    text = prepare_text(text)
    two_ch_combs = get_chars_combinations(text, 2)
    three_ch_combs = get_chars_combinations(text, 3)
    merged_ch_combs = merge_dicts(two_ch_combs, three_ch_combs)

    ru_similarity = 0
    bg_similarity = 0
    for comb in merged_ch_combs:
        if comb in similar_combs:
            if abs(merged_ch_combs[comb] - ru_ch_combs[comb]) < abs(merged_ch_combs[comb] - bg_ch_combs[comb]):
                ru_similarity += 1
            elif abs(merged_ch_combs[comb] - ru_ch_combs[comb]) > abs(merged_ch_combs[comb] - bg_ch_combs[comb]):
                bg_similarity += 1
            else:
                pass
    return {'ru': ru_similarity, 'bg': bg_similarity}


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    return {**dict1, **dict2}


def main():
    with open("OpenSubtitles.bg-ru.ru.txt", "r", encoding="utf-8") as f:
        ru_text = prepare_text(f.read())
    with open("OpenSubtitles.bg-ru.bg.txt", "r", encoding="utf-8") as f:
        bg_text = prepare_text(f.read())

    ru_two_ch_combs = get_chars_combinations(ru_text, 2)
    ru_three_ch_combs = get_chars_combinations(ru_text, 3)
    ru_merged_combs = merge_dicts(ru_two_ch_combs, ru_three_ch_combs)

    bg_two_ch_combs = get_chars_combinations(bg_text, 2)
    bg_three_ch_combs = get_chars_combinations(bg_text, 3)
    bg_merged_combs = merge_dicts(bg_two_ch_combs, bg_three_ch_combs)

    similar_combs = dict()
    for comb in ru_merged_combs:
        if comb in bg_merged_combs:
            similar_combs[comb] = abs(ru_merged_combs[comb] - bg_merged_combs[comb])

    ru_two_ch_combs = sorted(ru_two_ch_combs.items(), key=lambda item: item[1], reverse=True)
    ru_three_ch_combs = sorted(ru_three_ch_combs.items(), key=lambda item: item[1], reverse=True)
    print("Топ 30 часто встречающихся двоек и троек символов на русском языке: ")
    for i in range(30):
        print(ru_two_ch_combs[i], '|', ru_three_ch_combs[i])

    bg_two_ch_combs = sorted(bg_two_ch_combs.items(), key=lambda item: item[1], reverse=True)
    bg_three_ch_combs = sorted(bg_three_ch_combs.items(), key=lambda item: item[1], reverse=True)
    print("\nТоп 30 часто встречающихся двоек и троек символов на болгарском языке: ")
    for i in range(30):
        print(bg_two_ch_combs[i], '|', bg_three_ch_combs[i])

    similar_combs = {k: v for k, v in sorted(similar_combs.items(), key=lambda item: item[1], reverse=True)}
    print("\nДвойки и тройки символов, наиболее различающиеся по частоте употребления между языками:")
    for comb, diff in similar_combs.items():
        if diff >= 50:
            print(comb, ': ', diff, sep='')

    filenames = ("test_BG_1.txt", "test_RU_1.txt", "test_BG_2.txt", "test_RU_2.txt")
    print()
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as f:
            text = prepare_text(f.read())
        similarities = determine_text_language(text, similar_combs, ru_merged_combs, bg_merged_combs)
        if "RU" in filename:
            print(f"Был взят русский текст из файла {filename}")
        if "BG" in filename:
            print(f"Был взял болгарский текст из файла {filename}")
        if similarities["ru"] > similarities["bg"]:
            print("Программа определила текст как русский\n")
        elif similarities["ru"] < similarities["bg"]:
            print("Программа определила текст как болгарский\n")
        else:
            print("Программа не может определить на каком языке текст")


if __name__ == '__main__':
    main()
