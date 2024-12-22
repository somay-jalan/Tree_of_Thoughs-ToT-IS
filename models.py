import os
import openai
from openai import OpenAI
import backoff 
from dotenv import load_dotenv
import os
from together import Together


load_dotenv('config.env')
client=None


completion_tokens = prompt_tokens = 0



# @backoff.on_exception(backoff.expo, openai.error.OpenAIError)
def completions_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

def gpt(prompt, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    global client
    if("gpt" in model):
        api_key = os.getenv("OPENAI_API_KEY", "")
        client = OpenAI(api_key=api_key)
    elif("gemini" in model):
        api_key = os.getenv("Generative_Language_API_Key_gemini", "")
        client = OpenAI(api_key=api_key,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    elif("llama" or "Qwen" in model):
        api_key = os.getenv("TOGETHER_API_KEY", "")
        client = Together(api_key=api_key)
    else:
        api_key = os.getenv("TOGETHER_API_KEY", "")
        client = Together(api_key=api_key)
    if api_key != "":
        pass
    else:
        print("Warning: API_KEY is not set")

    api_base = os.getenv("OPENAI_API_BASE", "")
    if api_base != "":
        print("Warning: OPENAI_API_BASE is set to {}".format(api_base))
        # TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url=api_base)'
        # openai.api_base = api_base
    messages = [{"role": "user", "content": prompt}]
    return chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)

def chatgpt(messages, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    global completion_tokens, prompt_tokens
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        # print("INPUT MESSAGE:")
        # print(messages)
        res = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, n=cnt)
        
        outputs.extend([choice.message.content for choice in res.choices])
        print("RESPONSE:")
        print(outputs)
        # log completion tokens
        # completion_tokens += res.usage.completion_tokens
        # prompt_tokens += res.usage.prompt_tokens
        # print(outputs)
    return outputs




def gpt_usage(backend="gpt-4"):
    global completion_tokens, prompt_tokens
    if backend == "gpt-4":
        cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03
    elif backend == "gpt-3.5-turbo":
        cost = completion_tokens / 1000 * 0.002 + prompt_tokens / 1000 * 0.0015
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}
