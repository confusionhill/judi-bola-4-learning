from fastapi import FastAPI, Request

from routes.prediction.predictionController import router as predictionRouter
from services.machineLearning.machine_learning_service import ml_service
from routes.auth.authController import router as authRouter
from services.database.database_manager import conn

ml_service.onCreateMLService()
app = FastAPI()
app.include_router(predictionRouter)
app.include_router(authRouter)


@app.get("/")
async def root():
    return {"message": "hello hacker!"}

@app.get("/teams")
async def get_available_teams():
    result = conn.execute("SELECT * FROM Teams")
    teams = []
    for team in result:
        teams.append({"id": team[0], "name":team[1]})
    return {
        "teams": teams
    }


