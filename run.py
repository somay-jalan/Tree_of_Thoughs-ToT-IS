import argparse
from bfs import solve
from game24 import Game24Task
args = argparse.Namespace(backend="meta-llama/Llama-3.3-70B-Instruct-Turbo", temperature=0.7, task='game24', naive_run=False, prompt_sample=None, method_generate='propose', method_evaluate='value', method_select='greedy', n_generate_sample=1, n_evaluate_sample=3, n_select_sample=5)

task = Game24Task(model="meta-llama/Llama-3.3-70B-Instruct-Turbo")

benchmark=False
if benchmark:
    information_staring=False
    proper_prompt=False
    proper_prompt_with_information_sharing=False
    with open(f"log_{information_staring}_{proper_prompt}_{proper_prompt_with_information_sharing}.txt","w+") as file:
        for i in range(0,1362,100):
            ys, infos = solve(args, task, i,information_staring=information_staring,proper_prompt=proper_prompt,proper_prompt_with_information_sharing=proper_prompt_with_information_sharing)
            file.write(f'{i}:{infos}')
            file.wirte("\n")
            file.write("="*15)
            file.wirte("\n")
            file.flush()
else:
    ys, infos = solve(args, task, 500-1,information_staring=False,proper_prompt=False,proper_prompt_with_information_sharing=False)
    print(ys[0])