import os
import csv
from collections.abc import Iterator, Iterable


class Result:
    name: str = ""
    correct: bool = False
    status: str = ""
    time: float = 0.0
    mem: float = 0.0

    def __init__(self, name: str, correct: bool, status: str, time: float, mem: float):
        self.name = name
        self.correct = correct
        self.status = status
        self.time = time
        self.mem = mem


class ResultReader:
    def __init__(self, reader):
        self.reader = reader

    def __iter__(self) -> Iterator[Result]:
        return self

    def __next__(self) -> Result:
        line = next(self.reader)
        task_name = line[0]
        real_result = line[1]
        status = line[2]
        time = float(line[3])
        mem = float(line[5])

        isCorrect = False
        if real_result.startswith("true") and status.startswith("true"):
            isCorrect = True
        elif real_result.startswith("false") and status.startswith("false"):
            isCorrect = True

        return Result(task_name, isCorrect, status, time, mem)


def read_bench_result(file_path: os.PathLike) -> Iterable[Result]:
    # Read SV-Comp csv file and returns array:
    # [NameOfFile, isCorrect, status, time, mem]

    file = open(file_path)

    reader = csv.reader(file, delimiter='\t')

    # Skip first 3 lines
    for _ in range(3):
        next(reader)

    return iter(ResultReader(reader))
