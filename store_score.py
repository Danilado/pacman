import os.path

filename = "top_score.txt"
max_store = 5


def get_scores():
    with open(filename, "r", encoding="ascii") as file:
        for line in file:
            if line != "":
                yield int(line)


def clear_scores():
    open(filename, "w", encoding="ascii").close()


def store_score(score: int):
    if not os.path.exists(filename):
        clear_scores()
    scores = list(get_scores())[:(max_store-1)]
    scores.append(score)
    scores.sort(reverse=True)
    with open(filename, "w", encoding="ascii") as file:
        for score in scores:
            file.write(f"{score}\n")
