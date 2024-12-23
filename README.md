# Tree of Thoughts with Information sharing (TOT-IS)

This project implements the Tree of Thoughts (ToT) framework, a systematic exploration approach for language models to solve complex reasoning tasks through structured thought processes, but also sees if we share information between nodes for each tree is there any benefit for doing so. Also if we provide feedback to the nodes given by the judges does that help the nodes which are continuing to live and moving on with the next step. 


## Getting Started

To get started you need to clone this repo and create a "config.env" file and add api keys (if you would like to use that model):
openAI as OPENAI_API_KEY=API_KEY
gemini as Generative_Language_API_Key_gemini=API_KEY
together.ai TOGETHER_API_KEY=API_KEY.

and then run the run.py file. Depending on the model selected the API calls will be made accordingly. 
To be noted: The prompts and pipeline has not been tested on all models hosted on openAI, gemini and together.ai. They are tested on a handfull of models of llama, qwen, gemini and gpt. This is still a work in progress. 

The information_staring parameter in solve can be set to False and in that case the code works exactly the same as the code provided by tree of thoughts google deep mind paper though the prompts might be different if used for model other than GPT 3.5 and GPT 4 as Tree of Thoughts authors have only provided prompts for GPT models. In case it is set to True then, the infomation is shared between nodes or "ys" and prompts written by me with shared information is used. 


## Results
Currently as of updating this README (23 dec 2024) there is no improvement in sharing the infomation. There does not seem to be any downside but there also does not seem to be any improvement, by improvement what I mean is that if in a game of 24 if TOT is not able to solve any problem then TOT-IS also is not able to solve the problem, but if TOT is able to solve then TOT-IS is also able to solve. So no improvement.

## TO DO LIST:
1. Change the prompts: currently in the 1 shot proposal prompts, proposal prompts do not know that that they are playing a game of 24, I think if we provide them context of what game they are playing and then take step by step proposals, that should help but this ofcourse needs to be tested. 
2. Provide feedback given by value prompts back to the nodes. 
If nodes have information that they are playing game of 24 and get feedback from judges that from their current path it seems impossible that they can reach 24, then a node might want to change its step(s) and with information from the other nodes, it might also want to switch paths, needs to be implemented and tested. 
3. Try on creative writing task and crossword task as provided in tree of thoughts paper. 



## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or reach out to me at somay22505@iiitd.ac.in. Would love to hear your thoughts(no pun intended.)

