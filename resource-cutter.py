#!/usr/bin/python

from typing import Tuple
import read_results
import argparse
import os
from typing import Optional
from collections.abc import Iterator, Iterable


class ResourceRestrictedResultIterator:
    mem: Optional[float] = None
    time: Optional[float] = None

    it: Iterator[read_results.Result]

    def __init__(self, it: Iterator[read_results.Result], mem: Optional[float], time: Optional[float]):
        self.mem = mem
        self.time = time
        self.it = it

    def __iter__(self) -> Iterator[read_results.Result]:
        return self

    def __next__(self) -> read_results.Result:
        result = next(self.it)
        if result:
            if self.mem and self.mem <= result.mem:
                result.status = "unknown"
                result.correct = False
            if self.time and self.time <= result.time:
                result.status = "unknown"
                result.correct = False
                result.time = self.time

        return result


def filter_correct(it: Iterator[read_results.Result]) -> list[read_results.Result]:
    it = filter(lambda x: x.correct, it)
    return list(it)


def calc_time(it: Iterator[read_results.Result]) -> list[read_results.Result]:
    time = 0.0
    for r in it:
        time += r.time
    return time


def calc_mem(it: Iterator[read_results.Result]) -> list[read_results.Result]:
    mem = 0.0
    for r in it:
        mem += r.mem
    return mem


parser = argparse.ArgumentParser(
    prog="resource-cutter", description="Take 1 bench result and assume that all result that exceed resources is unknown")
parser.add_argument("file", action='store')
parser.add_argument("--time", action='store',
                    type=float, help="time restriction")
parser.add_argument("--mem", action='store',
                    type=float, help="memory restriction")
args = parser.parse_args()

reader_result = read_results.read_bench_result(args.file)
reader_result = ResourceRestrictedResultIterator(
    reader_result, args.mem, args.time)

print("Time:", calc_time(reader_result))
