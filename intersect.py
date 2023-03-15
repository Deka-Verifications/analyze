#!/usr/bin/python

import read_results
import argparse


def pairs(list):
    shifted_it = iter(list)
    next(shifted_it)
    return zip(list, shifted_it)


def get_correct_result_names(file_name: str) -> list[str]:
    reader_result = read_results.read_bench_result(file_name)
    reader_result = filter(lambda x: x.correct, reader_result)
    reader_result = map(lambda x: x.name, reader_result)
    return list(reader_result)


parser = argparse.ArgumentParser(
    prog="intersect", description="Take 2+ bench result and find intersect between CORRECT tasks")

parser.add_argument("files", action='store', nargs='+')

args = parser.parse_args()


for file1, file2 in pairs(args.files):
    correct1 = get_correct_result_names(file1)
    correct2 = get_correct_result_names(file2)
    print(len(set(correct1).intersection(correct2)))
