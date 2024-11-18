from transformers import pipeline
from huggingface_hub import login
import os
from dotenv import load_dotenv
import torch

#llama setup
# load_dotenv('.env')
# api_key = os.environ.get("huggingface_access")
# login(token=api_key)
# pipe = pipeline(task="text-generation", model="meta-llama/Llama-3.2-3B-Instruct")
# messages = [
#     {"role": "system", "content": '''
#     You are a helpful assistant that takes in weather, flood, airquality, and marine weather, you give someone 
#     advice on what precautions they should take for the day, and what qualities are related.
#         '''},
# ]

# def get_response(weather_dicts):
#     messages.append(
#         {"role": "user", "content": f"Weather is {weather_dicts['forecast']}, floor news is {weather_dicts['flood']}, marine health is {weather_dicts['marine']}, and the air quality is {weather_dicts['air-quality']}. What precautions should I take?"})
#     outputs = pipe(
#         messages,
#         max_new_tokens=256,
#     )
#     return outputs[0]["generated_text"][-1]