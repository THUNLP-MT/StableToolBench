import torch
import pandas as pd

import transformers
from transformers import pipeline
from accelerate import Accelerator

import json
from json import JSONDecodeError

from tqdm import tqdm
import argparse
import os
from vllm import LLM, SamplingParams

PROMPT="""
gpt-4-turbo

Given a query and an answer provided by an AI agent, you now need to determine the answer_status of whether the well solved the query, i.e. whether the need of the query is satisfied. You need to output "Unsolved" or "Solved" and your reason. You must obey the following rules:

You should response "Solved" when:
    1. If the answer well provides the information needed by the query, then it is "Solved". The answer does not need to be perfect, and it only needs to make a genuine attempt to address the query.
	2.	Consider only Completeness:
	    •	The answer attempts to address every part of the query, regardless of whether the information provided is factually correct or accurate, unless there is a severe factual error.
	3.	For Multi-part Queries:
	    •	For queries with multiple parts, all parts must be addressed for the answer to be considered “Solved”.
	4.	Genuine Attempt :
	    •	The answer makes a genuine attempt to provide the requested information or perform the requested task for all parts of the query. This includes scenarios where the answer concludes that “nothing” is a reasonable response (e.g., when the requested information does not exist or is not available, or a possible answer of the query is nothing and the model answers nothing after reasonable attempts).

You should response "Unsolved" when:
    1.	Refusal, Apology, or Non-engagement:
	    •	The answer includes a refusal or apology (e.g., “I'm sorry, I can't help with that”).
	    •	The answer does not directly engage with or address the query in any way.
	2.	Multi-part Queries:
	    •	If the query has multiple parts and at least one part is not well addressed.
    3. Severe Factual Error:
        •   If the answer contains a severe factual error that significantly impacts the usefulness of the information provided.


Additional Guidelines:
    1. VERY IMPORTANT: DO NOT BE TOO HARSH. The model does not need to be perfect, and the answer does not need to be flawless. It only needs to make a genuine attempt to address the query.
    1. DO NOT evaluate factual accuracy or correctness of the information provided based on your knowledge. Assume that the information provided is accurate and focus solely on whether the answer attempts to address all parts of the query, unless there is a severe factual error that conficts common knowledge.
	2.	Focus on Final Answer: Only the final answer is provided and should be considered, disregarding any processes that were used to generate the answer. You only need to judge whether the information need is satisfied.
	3.	Answer Completion: The agent does not need to detail how it arrived at the answer, only that the answer itself is complete and attempts to address the query.

Here are some examples:

Query 1: I'm planning a movie night with my friends and we want to watch a horror film. Can you recommend some popular horror movies available on streaming platforms in the US? Also, provide the runtime and IMDb ratings for these movies.
Answer 1: Here are some popular horror movies available on streaming platforms in the US:\n\n1. Knives Out\n   - Runtime: 130 minutes\n   - IMDb Rating: 7.9/10\n   - Available on: Netflix, Prime Video, Hulu, Amazon Prime Video\n\n2. Jumanji: The Next Level\n   - Runtime: 110 minutes\n   - IMDb Rating: 6.7/10\n   - Available on: Hulu, Amazon Prime Video, Netflix\n\nPlease note that availability may vary depending on your location and streaming platform subscriptions. Enjoy your movie night!
Answer Status: Solved0304
Reason: The answer addressed all parts of subqueries by providing a list of popular horror movies available on streaming platforms in the US, along with their runtime and IMDb ratings. Whether the film is horror is a factual matter that does not to be checked.

Query 2: I'm a screenwriter looking for inspiration for my next project. Can you help me find a list of critically acclaimed movies available on streaming platforms in the US? Also, provide me with the streaming sources for the movie 'Citizen Kane' and the basic information about the cast, including their names and professions.
Answer 2: The movie 'Citizen Kane' is available on the following streaming platforms:
- HBO Max: [Watch on HBO Max](https://play.hbomax.com/feature/urn:hbo:feature:GXduU_gwwz-NvjAEAAAAC)
- Amazon Prime Video: [Watch on Amazon Prime Video](https://www.amazon.com/Citizen-Kane-Orson-Welles/dp/B000I9YLWG)
- AppleTV+: [Watch on AppleTV+](https://tv.apple.com/us/movie/citizen-kane/umc.cmc.21zj0v11gnqbbqrebieh0vpk7)
- Disney+: Available on Disney+
- Netflix: Available on Netflix
Answer Status: Unsolved
Reason: The answer only addressed the first and second part of the query by providing the streaming sources for the movie 'Citizen Kane' but did not provide information about the cast or a list of critically acclaimed movies available on streaming platforms in the US. The response was incomplete and did not fully address the query.

Query: 
{query}
Answer: 
{answer}

Now give your reason and answer status in the following format:

Answer Status
xxx (can only be "Solved" or "Unsolved")
Reason
xxx
"""

# /root/.cache/huggingface/accelerate/default_config.yaml
# MODEL_PATH = "/yeesuanAI05/thumt/gzc/LLaMA-Factory/out/v3.1"
# TEST_PATH = "/yeesuanAI05/thumt/gzc/stb/train/test_eval_ochat.0.jsonl"
# HUMAN_PATH = "/yeesuanAI05/thumt/gzc/human_eval.csv"
# DEVICE  = "cuda"

def parse_args():
    parser = argparse.ArgumentParser(description="demo")

    parser.add_argument("--model_path", type=str)
    parser.add_argument("--evaluation_path", type=str)
    parser.add_argument("--output_path", type=str)
    parser.add_argument("--evaluated", action="store_true")
    parser.add_argument("--ids", type=str, default=None)

    return parser.parse_args()


def run_human_eval():
    test = pd.read_csv(HUMAN_PATH)
    pipeline = transformers.pipeline(
        "text-generation", model=MODEL_PATH, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto"
    )

    df = {
        "prompt" : [],
        "r1" : [],
        "r2" : [],
        "model" : []
    }
    df = pd.DataFrame(df)

    for i in tqdm(range(len(test))):
        df.loc[len(df)] = [
            "gpt-4-turbo\n" + test["prompt"][i],
            test["r1"][i],
            test["r2"][i],
            pipeline("gpt-4-turbo\n" + test["prompt"][i], max_length=2000, num_return_sequences=1, do_sample=True, top_p=0.95)[0]['generated_text']
        ]
    
    df.to_csv(MODEL_PATH + "model_human_eval.csv", index=False)

def get_response(text):
    text = text.lower().strip()
    
    if "unsolved" in text:
        return 0
    elif "solved" in text:
        return 1
    else:
        return 0
            
def main(args):
    if args.evaluated is not True:
        # pipeline = transformers.pipeline("text-generation", model=args.model_path, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto")
        llm = LLM(model=args.model_path)
        sampling_params = SamplingParams(temperature=0, max_tokens=512)
        data = []
        with open(args.evaluation_path, "r") as f:
            data = json.load(f)
        with open(args.ids, "r") as f:
            ids = list(json.load(f).keys())
        out = {
            "query" : [],
            "final_answer" : [],
            "evaluation" : [],
            "prompt" : []
        }

        for key in tqdm(ids):
            final_answer = data[key]["answer"]["final_answer"]
            if final_answer != "":
                if key not in data:
                    import pdb; pdb.set_trace()
                query = data[key]['query']

                if final_answer.startswith("{\\"):
                    final_answer = json.loads(final_answer)["final_answer"]
                else:
                    final_answer = final_answer

                prompt = PROMPT.format(query=query, answer=final_answer)
                message = [{
                    "role": "user",
                    "content": prompt
                }]
                evaluation = llm.chat(message, sampling_params, use_tqdm=False)
                evaluation = evaluation[0].outputs[0].text
                out["query"].append(query)
                out["final_answer"].append(final_answer)
                out["evaluation"].append(evaluation)

                out["prompt"].append(prompt)
            
            else:
                query = data[key]['query']
                final_answer = "final_answer was not properly loaded"
                evaluation = "an error has occured"
                prompt = "an error has occured"
                

                out["query"].append(query)
                out["final_answer"].append(final_answer)

                evaluation = 'Answer Status: \nUnsolved\nReason: Parsing error'
                out["evaluation"].append(evaluation)
                out["prompt"].append(prompt)

        out = pd.DataFrame(out)
        out.to_csv(os.path.join(args.output_path), index=False)

    df = pd.read_csv(os.path.join(args.output_path))
    result = [get_response(df['evaluation'][i]) for i in range(len(df))]
    print(f"{os.path.basename(args.evaluation_path).split('.')[0]} has an success rate of {float(sum(result)) / float(len(result))}")

if __name__ == "__main__":
    args = parse_args()
    print(args)
    main(args)
    