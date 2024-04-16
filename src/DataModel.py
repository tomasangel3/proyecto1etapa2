from pydantic import BaseModel

class DataModel(BaseModel):
    Review: str
# Estas varibles permiten que la librería pydantic haga el parseo entre el Json recibido y el modelo declarado.

#Esta función retorna los nombres de las columnas correspondientes con el modelo esxportado en joblib.
    def columns(self):
        return ["Review"]
