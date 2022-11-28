from fastapi import FastAPI, HTTPException

from model.predictionModel import TeamPlaying, PredictionModel
from services.machineLearning.machine_learning_service import ml_service


def predict_winner(playing: TeamPlaying) -> dict:
    try:
       return ml_service.predictResult(playing).dict()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Prediction Cannot be Generated")