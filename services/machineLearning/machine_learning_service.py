import joblib
import numpy as np
import pandas as pd

from model.predictionModel import TeamPlaying, PredictionModel
from services.database.database_manager import conn


class MLService:
    ranking = None
    final = None
    logreg = None

    def onCreateMLService(self):
        filename = "services/machineLearning/wcpredict2.pkl"
        loadedModel = joblib.load(filename)
        results = pd.read_csv('services/machineLearning/dataset/results.csv')
        winner = []
        for i in range(len(results['home_team'])):
            if results['home_score'][i] > results['away_score'][i]:
                winner.append(results['home_team'][i])
            elif results['home_score'][i] < results['away_score'][i]:
                winner.append(results['away_team'][i])
            else:
                winner.append('Tie')
        results['winning_team'] = winner

        # column for goal difference in matches
        results['goal_difference'] = np.absolute(results['home_score'] - results['away_score'])

        results.head()
        wc_teams = [ 'Qatar', 'Senegal', 'Netherlands', 'Ecuador',
                     'England', 'USA', 'Iran', 'Wales',
                     'Argentina', 'Mexico', 'Poland','Saudi Arabia',
                     'France', 'Denmark', 'Tunisia', 'Australia',
                     'Japan', 'Spain', 'Germany', 'Costa Rica',
                     'Belgium', 'Croatia', 'Morocco', 'Canada',
                     'Brazil', 'Cameroon', 'Potter', 'Switzerland',
                     'Ghana', 'Uruguay', 'Korea Republic', 'Portugal'
                     ]

        df_teams_home = results[results['home_team'].isin(wc_teams)]
        df_teams_away = results[results['away_team'].isin(wc_teams)]
        df_teams = pd.concat((df_teams_home, df_teams_away))
        df_teams.drop_duplicates()
        year = []
        for row in df_teams['date']:
            year.append(int(row[:4]))
        df_teams['match_year'] = year

        # Slicing the dataset
        df_teams30 = df_teams[df_teams.match_year >= 1930]
        df_teams30 = df_teams30.drop(
            ['date', 'home_score', 'away_score', 'tournament', 'city', 'country', 'goal_difference', 'match_year'],
            axis=1)
        df_teams30 = df_teams30.reset_index(drop=True)
        df_teams30.loc[df_teams30.winning_team == df_teams30.home_team, 'winning_team'] = 2
        df_teams30.loc[df_teams30.winning_team == 'Tie', 'winning_team'] = 1
        df_teams30.loc[df_teams30.winning_team == df_teams30.away_team, 'winning_team'] = 0
        final = pd.get_dummies(df_teams30, prefix=['home_team', 'away_team'], columns=['home_team', 'away_team'])
        ranking = pd.read_csv(
            'services/machineLearning/dataset/us.csv')
        # asignment
        self.logreg = loadedModel
        self.ranking = ranking
        self.final = final

    def predictResult(self,playing: TeamPlaying) -> PredictionModel:
        positions = []
        result = conn.execute("SELECT * FROM Teams WHERE id")
        matches = [(playing.teamA, playing.teamB)]
        # Get team position on fifa ranking
        for match in matches:
            positions.append(self.ranking.loc[self.ranking['Team'] == match[0], 'Position'].iloc[0])
            positions.append(self.ranking.loc[self.ranking['Team'] == match[1], 'Position'].iloc[0])
        pred_set = []
        i = 0
        j = 0
        while i < len(positions):
            dict1 = {}
            if positions[i] < positions[i + 1]:
                dict1.update({'home_team': matches[j][0], 'away_team': matches[j][1]})
            else:
                dict1.update({'home_team': matches[j][1], 'away_team': matches[j][0]})
            pred_set.append(dict1)
            i += 2
            j += 1

        pred_set = pd.DataFrame(pred_set)
        backup_pred_set = pred_set
        pred_set = pd.get_dummies(pred_set, prefix=['home_team', 'away_team'], columns=['home_team', 'away_team'])
        missing_cols2 = set(self.final.columns) - set(pred_set.columns)
        for c in missing_cols2:
            pred_set[c] = 0
        pred_set = pred_set[self.final.columns]
        pred_set = pred_set.drop(['winning_team'], axis=1)
        return self.predict(pred_set, backup_pred_set, playing)

    def predict(self, pred_set, backup_pred_set, playing) -> PredictionModel:
        predictions = self.logreg.predict(pred_set)
        for i in range(len(pred_set)):
            result = "Tie"
            if predictions[i] == 2:
                result = backup_pred_set.iloc[i, 1]
            elif predictions[i] == 0:
                result = backup_pred_set.iloc[i, 0]
            return PredictionModel(teamA=playing.teamA,result=result, teamB=playing.teamB, teamAProb=self.logreg.predict_proba(pred_set)[i][2], teamBProb=self.logreg.predict_proba(pred_set)[i][0],
                               drawProb=self.logreg.predict_proba(pred_set)[i][1])


ml_service = MLService()
