import csv
import os.path
from dataclasses import dataclass, astuple
from datetime import datetime

from globalvars import datetime_format

filename = "top_score.csv"
max_store = 5


@dataclass
class Score:
    datetime: datetime
    nickname: str
    score: int


def get_scores():
    if not os.path.exists(filename):
        clear_scores()
    with open(filename, "r", encoding="ascii") as file:
        reader = csv.reader(file)
        for line in reader:
            if len(line) >= 3:
                yield Score(datetime.strptime(line[0], datetime_format), line[1], int(line[2]))
            else:
                # print("invalid line", line)
                pass


def clear_scores():
    open(filename, "w", encoding="ascii").close()


def store_score(score: int, nickname: str):
    if not os.path.exists(filename):
        clear_scores()
    scores = list(get_scores())[:(max_store - 1)]
    scores.append(Score(datetime.today(), nickname, score))
    scores.sort(key=lambda item: item.score, reverse=True)
    # print(scores)
    with open(filename, "w", encoding="ascii") as file:
        writer = csv.writer(file)
        for date_and_time, nickname, score in [astuple(score) for score in scores]:
            writer.writerow((date_and_time.strftime("%d.%m.%Y %H:%M:%S"), nickname, score))
