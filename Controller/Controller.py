from .QuestionClassifier import QuestionClassifier
from .AppExecutor import AppExecutor

class Controller:
        
    def propagete(self, question) :
        q_type = QuestionClassifier().classify(question)
        response = AppExecutor().ExecuteApp(q_type, question)
        return response