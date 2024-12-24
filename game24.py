import re
import os
import sympy
import pandas as pd
from base import Task, DATA_PATH


def get_current_numbers(y: str) -> str:
    last_line = y.strip().split('\n')[-1]
    return last_line.split('left: ')[-1].split(')')[0]

def proper_prompt(x:str,y:str)->str:
    steps=y.strip().split('\n')
    prompt = x+"\n"
    for i,step in enumerate(steps):
        prompt+=f'{i+1}. {step}\n'
    return prompt

class Game24Task(Task):
    """
    Input (x)   : a string of 4 numbers
    Output (y)  : a trajectory of 3 steps to reach 24
    Reward (r)  : 0 or 1, depending on whether the trajectory is correct
    Input Example: 
        1 2 3 4
    Output Example: 
        1 + 2 = 3 (left: 3 3 4)
        3 + 3 = 6 (left: 4 6)
        6 * 4 = 24 (left: 24)
        (1 + 2 + 3) * 4 = 24
    """
    def __init__(self,model, file='24.csv'):
        global standard_prompt,cot_prompt,propose_prompt,value_last_step_prompt,value_prompt,propose_prompt_with_information_sharing,proper_propose_prompt
        """
        file: a csv file (fixed)
        """
        super().__init__()
        # path = os.path.join(DATA_PATH, '24', file)
        path=file
        self.data = list(pd.read_csv(path)['Puzzles'])
        self.value_cache = {}
        self.steps = 4
        # self.stops = ['\n'] * 4
        if "gemini" in model:
            from game24_prompts_gemini import  standard_prompt,cot_prompt,propose_prompt,value_last_step_prompt,value_prompt,propose_prompt_with_information_sharing
        elif "gpt" in model:
            from game24_prompts_gpt import  standard_prompt,cot_prompt,propose_prompt,value_last_step_prompt,value_prompt,propose_prompt_with_information_sharing
        elif "llama" in model:
            from game24_prompts_llama_qwen import  standard_prompt,cot_prompt,propose_prompt,value_last_step_prompt,value_prompt,propose_prompt_with_information_sharing,proper_propose_prompt
        else:
            from game24_prompts_llama_qwen import  standard_prompt,cot_prompt,propose_prompt,value_last_step_prompt,value_prompt,propose_prompt_with_information_sharing,proper_propose_prompt




    def __len__(self) -> int:
        return len(self.data)
    
    def get_input(self, idx: int) -> str:
        return self.data[idx]

    def test_output(self, idx: int, output: str):
        expression = output.strip().split('\n')[-1].lower().replace('answer: ', '').split('=')[0]
        numbers = re.findall(r'\d+', expression)
        problem_numbers = re.findall(r'\d+', self.data[idx])
        if sorted(numbers) != sorted(problem_numbers):
            return {'r': 0}
        try:
            # print(sympy.simplify(expression))
            return {'r': int(sympy.simplify(expression) == 24)}
        except Exception as e:
            # print(e)
            return {'r': 0}
            
    @staticmethod
    def standard_prompt_wrap(x: str, y:str='') -> str:
        return standard_prompt.format(input=x) + y

    @staticmethod
    def cot_prompt_wrap(x: str, y:str='') -> str:
        return cot_prompt.format(input=x) + y
    
    @staticmethod
    def propose_prompt_wrap(x: str, y: str='') -> str:
        current_numbers = get_current_numbers(y if y else x)
        if current_numbers == '24':
            prompt = cot_prompt.format(input=x) + 'Steps:' + y
            # print([prompt])
        else:
            prompt = propose_prompt.format(input=current_numbers)
        return prompt
    
    @staticmethod
    def propose_prompt_with_information_wrap(x: str,y:str, information: str='') -> str:
        current_numbers = get_current_numbers(y if y else x)
        if current_numbers == '24':
            prompt = cot_prompt.format(input=x) + 'Steps:' + y
            # print([prompt])
        else:
            prompt = propose_prompt_with_information_sharing.format(input=current_numbers,information_input=information)
        return prompt

    @staticmethod
    def proper_propose_prompt_wrap(x: str,y:str,step:int) -> str:
        current_numbers = get_current_numbers(y if y else x)
        if current_numbers == '24':
            prompt = cot_prompt.format(input=x) + 'Steps:' + y
            # print([prompt])
        else:
            prompt = proper_propose_prompt.format(input=proper_prompt(x,y),step=step+1)
        return prompt
    
    @staticmethod
    def value_prompt_wrap(x: str, y: str) -> str:
        last_line = y.strip().split('\n')[-1]
        if 'left: ' not in last_line:  # last step
            ans = last_line.lower().replace('answer: ', '')
            # print([value_last_step_prompt.format(input=x, answer=ans)])
            return value_last_step_prompt.format(input=x, answer=ans)
        current_numbers = get_current_numbers(y)
        return value_prompt.format(input=current_numbers)
    
    @staticmethod
    def value_outputs_unwrap(x: str, y: str, value_outputs: list) -> float:
        if len(y.strip().split('\n')) >= 4 and 'answer' not in y.lower():
            return 0
        value_names = [_.split('\n')[-1] for _ in value_outputs]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value