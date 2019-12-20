from .QuestionClassifier.QuestionClassifier import QuestionClassifier
from .AppExecutor import AppExecutor

class Controller:  

    def __init__(self, **kwargs) :
        '''
        to-do : kwargs로 qc_type='rnn'혹은 'regex'를 입력 받아서 
        _qc를 인공지능 혹은 정규표현식 엔진으로 설정한다
        '''
        self._qc = QuestionClassifier()

    def propagate(self, question) :

        q_type = self._qc.classify(question)
        response = AppExecutor().ExecuteApp(q_type, question)
        return response