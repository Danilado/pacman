import csv
import os
from dataclasses import dataclass

import global_variables

filename = "saves/settings.csv"
_settings_cache = None


@dataclass
class Settings:
    difficulty: float
    cell_size: int


def clear_settings():
    open(filename, "w", encoding="utf-8").close()


def get_settings():
    global _settings_cache
    if _settings_cache is None:
        if not os.path.exists(filename):
            clear_settings()
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for line_num, line in enumerate(reader):
                if len(line) >= 2:
                    result = Settings(float(line[0]), int(line[1]))
                    _settings_cache = result
                    return result
                elif global_variables.debug:
                    print(f"[WARNING] Can not parse {filename}:{line_num} {line}")
    else:
        return _settings_cache


def store_settings():
    if not os.path.exists(filename):
        clear_settings()
    with open(filename, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow((str(global_variables.difficulty), str(global_variables.cell_size)))
    global _settings_cache
    _settings_cache = Settings(global_variables.difficulty, global_variables.cell_size)
