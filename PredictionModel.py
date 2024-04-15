from joblib import load

class Model:

    def __init__(self,columns):
        self.model = load('/Users/tomasangel/Documents/GitHub/proyecto1etapa2/data/modelo.joblib')

    def make_predictions(self, data):
        result = self.model.predict(data)
        return result
