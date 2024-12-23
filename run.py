import argparse
from bfs import solve
from game24 import Game24Task
args = argparse.Namespace(backend="Qwen/Qwen2.5-72B-Instruct-Turbo", temperature=0.7, task='game24', naive_run=False, prompt_sample=None, method_generate='propose', method_evaluate='value', method_select='greedy', n_generate_sample=1, n_evaluate_sample=3, n_select_sample=3)

task = Game24Task(model="Qwen/Qwen2.5-72B-Instruct-Turbo")
ys, infos = solve(args, task, 1000-1,information_staring=True)
print(ys[0])