from openai import OpenAI
from dotenv import load_dotenv
import json
from response_format import response_format
from system_prompts import justInTimeInventoryPrompt
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

client = OpenAI()

inputParams = {
    "productType": "Electronics",
    "currentInventoryLevel": 100,
    "averageLeadTime": 5,
    "dailyDemand": 10,
    "productionDays": 10
}


@app.post("/api/v1/just-in-time-inventory")
async def just_in_time_inventory(request: Request):
    try:

        inputParameters = await request.json()

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=justInTimeInventoryPrompt(
                inputParameters=inputParameters),

            response_format=response_format
        )

        response = json.loads(completion.choices[0].message.content)

        return {"success": True, "results": response["results"]}

    except Exception as e:
        return {"success": False, "message": str(e)}
