#!/usr/bin/python

from typing import Tuple
import read_results
import argparse
import os

import matplotlib.pyplot as plt


def get_sorted_by_time(file_name: str, mem: bool) -> list[read_results.Result]:
    reader_result = read_results.read_bench_result(file_name)
    reader_result = filter(lambda x: x.correct, reader_result)

    def proj_func(x): return x.time
    if mem:
        def proj_func(x): return x.mem

    reader_result = map(proj_func, reader_result)
    return sorted(reader_result)


parser = argparse.ArgumentParser(
    prog="qqplot", description="Take 2+ bench result and plot q-q")
parser.add_argument("files", action='store', nargs='+')
parser.add_argument("--mem", action='store_true',
                    help="Build plot for memory instead cputime")
args = parser.parse_args()

style_id = 0
plot_styles = ["-b", "--r", "-.g"]

for file in args.files:
    file_name = os.path.basename(file)
    file_name = file_name.split(".")[0]

    plot_style = plot_styles[style_id % len(plot_styles)]

    results = get_sorted_by_time(file, args.mem)
    plt.plot(results, plot_style, label=file_name)
    plt.legend()

    style_id += 1

plt.yscale("log")
plt.xlabel("Число задач")
if args.mem:
    plt.ylabel("Минимальная память для достижения")
else:
    plt.ylabel("Минимальное время для достижения")
plt.show()
