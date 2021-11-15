import csv
import os.path

filename = "top_score.csv"
max_store = 5


def get_scores():
    if not os.path.exists(filename):
        clear_scores()
    with open(filename, "r", encoding="ascii") as file:
        reader = csv.reader(file)
        for line in reader:
            if len(line) >= 2:
                yield line[0], int(line[1])
            else:
                # print("invalid line", line)
                pass


def clear_scores():
    open(filename, "w", encoding="ascii").close()


def store_score(score: int, nickname: str):
    if not os.path.exists(filename):
        clear_scores()
    scores = list(get_scores())[:(max_store-1)]
    scores.append((nickname, score))
    scores.sort(key=lambda item: item[1], reverse=True)
    print(scores)
    with open(filename, "w", encoding="ascii") as file:
        writer = csv.writer(file)
        for nickname, score in scores:
            writer.writerow((nickname, score))
