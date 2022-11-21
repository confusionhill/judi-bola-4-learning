from fastapi import FastAPI, Request

from routes.prediction.predictionController import router as predictionRouter
from services.machineLearning.machine_learning_service import ml_service
from routes.auth.authController import router as authRouter

ml_service.onCreateMLService()
app = FastAPI()
app.include_router(predictionRouter)
# app.include_router(authRouter)


@app.get("/")
async def root():
    return {"message": "hello hacker!"}

@app.get("/teams")
async def getAvailableTeams():
    return {
        "teams": [ 'Qatar', 'Senegal', 'Netherlands', 'Ecuador',
                     'England', 'USA', 'Iran', 'Wales',
                     'Argentina', 'Mexico', 'Poland','Saudi Arabia',
                     'France', 'Denmark', 'Tunisia', 'Australia',
                     'Japan', 'Spain', 'Germany', 'Costa Rica',
                     'Belgium', 'Croatia', 'Morocco', 'Canada',
                     'Brazil', 'Cameroon', 'Potter', 'Switzerland',
                     'Ghana', 'Uruguay', 'Korea Republic', 'Portugal'
                     ]
    }


