from openai import OpenAI
from dotenv import load_dotenv
from system_prompts import justInTimeInventoryPrompt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from input_types import JustInTimeInventoryInputParamsType
from output_types import AnalysisResults

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

sampleInputParameters = {
    "productType": "Electronics",
    "currentInventoryLevel": 100,
    "averageLeadTime": 5,
    "dailyDemand": 10,
    "productionDays": 10
}


@app.post("/api/v1/just-in-time-inventory")
async def just_in_time_inventory(inputParameters: JustInTimeInventoryInputParamsType) -> AnalysisResults:

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=justInTimeInventoryPrompt(
            inputParameters=inputParameters),
        response_format=AnalysisResults
    )

    response = completion.choices[0].message.parsed

    return response
