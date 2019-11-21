from .QuestionClassifier import QuestionClassifier
from .AppExecutor import AppExecutor

class Controller:
        
    def propagate(self, question) :
        
        q_type = QuestionClassifier().classify(question)
        response = AppExecutor().executeApp(q_type, question)
        return response