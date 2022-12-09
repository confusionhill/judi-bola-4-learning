from fastapi import FastAPI
from routes.judi.judiController import router as judiRouter
from routes.prediction.predictionController import router as predictionRouter
from services.machineLearning.machine_learning_service import ml_service
from routes.auth.authController import router as authRouter, app as validator_app
from routes.user.user_controller import router as userRouter
from routes.team.team_controller import router as teamRouter
from services.database.database_manager import conn
from sqlalchemy.sql import text
import datetime
import pytz

ml_service.onCreateMLService()
app = FastAPI()
app.include_router(predictionRouter)
app.include_router(userRouter)
app.include_router(authRouter)
app.include_router(judiRouter)
app.include_router(teamRouter)
app.mount("/arga", validator_app)

@app.get("/")
async def root():
    dtime = datetime.datetime.now()
    timezone = pytz.timezone("Asia/Bangkok")
    dtzone = timezone.localize(dtime)
    return {
        "msg": "Hello Hacker :V ;)",
        "access-time": dtzone,
        "ps": "There's a secret!"
    }



