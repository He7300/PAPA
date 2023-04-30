import openai
from fastapi import FastAPI
from fastapi.responses import FileResponse
from typing import Optional
from matplotlib import pyplot as plt
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import sys

# Add the directory to the sys.path list
sys.path.append('E:\PAPACODE')

from dataScraper import get_response

app = FastAPI()

origins = ["*"]
key = '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'

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
messages = [{"role": "system",
             "content": f"You are an AI designed to give information in a specific format about a given plant, this information will include tips and warnings based on the local weather and the plant species"}]

openai.api_key = key

def get_plant_details(name):
    chat_log = [{
        'role': 'system',
        'content': r'Can you provide me with a list of important characteristics to know about the following plant?'
                   r' These can include information about its appearance, growth habits, reproduction, environmental requirements, and any other important features. Please provide the information in a clear and concise list format.',
    }, {'role': 'user', 'content': name}]
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=chat_log, max_tokens=100)
    answer = response.choices[0]['message']['content']
    return answer

@app.get("/images/{image_path:path}")
async def read_image(image_path: str, size: Optional[str] = None):
    image_file = f"images/{image_path}"
    if size is not None:
        image_file = f"images/{size}/{image_path}"
    return FileResponse(image_file)

@app.get("/generate_graph/{x}/{y}")
async def generate_graph(x:str,y:str):
    # Define the x and y values to plot
    x = [int(num) for num in x.split(',')]
    y = [int(num) for num in y.split(',')]

    # Create a new figure and axis object using matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the x and y values on the axis object
    ax.plot(x, y, color='red', linewidth=2, linestyle='--', marker='o', markersize=8)

    # Set the axis labels and title
    ax.set_xlabel('days', fontsize=14)
    ax.set_ylabel('Points', fontsize=14)
    ax.set_title('Ranking Progress', fontsize=16)

    # Set the axis ticks and limits
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_yticks([0, 10, 20, 30, 40])
    ax.set_xlim([0.5, 5.5])
    ax.set_ylim([0, 40])

    # Add a grid to the plot
    ax.grid(color='gray', linestyle='--', linewidth=0.5)


    # Add a legend to the plot
    ax.legend(['Data'], loc='upper right')

    # Save the figure to a file
    filename = "line_plot.png"
    plt.savefig(filename)

    # Close the figure to free up memory
    plt.close()

    # Return the saved image file as a FastAPI response
    return FileResponse(filename)

class ChatMessage(BaseModel):
    message: str
    sender: Optional[str] = None
    timestamp: Optional[str] = None

@app.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
    chat_log = [{
        'role': 'system',
        'content': r'You are an AI language model that is extremely knowledgeable about plants, deeply loves ecology, and is passionate about everything related to saving the environment. Please provide information about the importance of plants, their role in maintaining ecological balance, and some practical tips for individuals to contribute to environmental conservation. you must be really concise.',
    }, {'role': 'user', 'content': chat_message.message}]
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=chat_log, max_tokens=100)
    answer = response.choices[0]['message']['content']
    response = {
        "sender": "bot",
        "message": answer,
        "timestamp": chat_message.timestamp,
    }
    return response



@app.get("/plant/{plant_name}/{extension}")
async def plant(plant_name, extension):
    print(plant_name)
    img_path = r'C:\Users\He\Documents\dragonHacks\images' + '\\' + plant_name +'.'+ extension
    d_plant = get_response(img_path)
    chat_log = [{
        'role': 'system',
        'content': r'Can you provide me with a list of important characteristics to know about the following plant?'
                   r' These can include information about its appearance, growth habits, reproduction, environmental requirements, and any other important features. Please provide the information in a clear and concise list format.',
    }, {'role': 'user', 'content': d_plant[0]}]
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=chat_log, max_tokens=100)
    plant_details = response.choices[0]['message']['content'].replace('\n', '<br>')

    return plant_details
    # Return the plant details in the response
    # return {"plant_details": plant_details}

# my_plant = f"my plant is the species {results}"
# messages.append({"role": "user", "content": my_plant})
# preprompt1 = f"only refer to my plant by its common name"
# messages.append({"role": "user", "content": preprompt1})
# weatherpre = f"the current weather for my area is {weather['main']} with a temperature of {gen['temp']} fahrenheit and a humidity of {gen['humidity']} RH"
# messages.append({"role": "user", "content": weatherpre})
#
# message = input()
#
# messages.append({"role": "user", "content": message})
# response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=50)
# reply = response["choices"][0]["message"]["content"]
# messages.append({"role": "assistant", "content": reply})


@app.get("/")
async def main():
    return {"Hello": "World"}

if __name__ == "__main__":
    main()
