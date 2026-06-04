from fastapi import FastAPI
from fastapi import Request
from pydantic import BaseModel , Field ,  field_validator
import pandas as pd
import joblib
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("irrigation_model.pkl")


class IrrigationInput(BaseModel):
    Soil_Type: str
    Soil_Moisture: float = Field(..., ge=0 , le=100)
    Temperature_C: float
    Humidity: float = Field(..., ge=0 , le= 100)
    Rainfall_mm: float = Field(..., gt=0)
    Sunlight_Hours: float = Field(..., ge=0 , le=24)
    Wind_Speed_kmh: float = Field(..., gt=0)
    Crop_Type: str
    Previous_Irrigation_mm: float = Field(..., gt=0)

    @field_validator("Crop_Type")
    @classmethod
    def format_soil_type(cls, v: str):
        return v.strip().lower().capitalize()
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": "Invalid input. Please check your values.",
            "errors": exc.errors()
        },
    )

@app.get("/")
def home():
    return {"message": "Irrigation Prediction API Running"}


@app.post("/predict")
def predict(data: IrrigationInput):

    input_data = pd.DataFrame([{
        "Soil_Type": data.Soil_Type,
        "Soil_Moisture": data.Soil_Moisture,
        "Temperature_C": data.Temperature_C,
        "Humidity": data.Humidity,
        "Rainfall_mm": data.Rainfall_mm,
        "Sunlight_Hours": data.Sunlight_Hours,
        "Wind_Speed_kmh": data.Wind_Speed_kmh,
        "Crop_Type": data.Crop_Type,
        "Previous_Irrigation_mm": data.Previous_Irrigation_mm
    }])

    prediction = model.predict(input_data)[0]

    return {
        "irrigation_need": prediction
    }