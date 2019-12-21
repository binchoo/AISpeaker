from .QuestionClassifier.QuestionClassifier import QuestionClassifier
from .AppExecutor import AppExecutor

class Controller:  

    def __init__(self, **kwargs) :
        '''
        to-do : kwargs로 type='rnn'혹은 'regex'를 입력 받아서 
        _qc를 인공지능 혹은 정규표현식 엔진으로 설정한다
        default : type='rnn', upgrade=False
        '''
        if 'type' in kwargs.keys() :
            set_type = kwargs['type']
        else :
            set_type = 'rnn'
        self._qc = QuestionClassifier()
        self._qc.setClassifier(set_type)

        if 'upgrade' in kwargs.keys() :
            if kwargs['upgrade'] :
                self._qc.versionUp()
    
    def propagate(self, question) :

        q_type = self._qc.classify(question)
        print(q_type)
        response = AppExecutor().ExecuteApp(q_type, question)
        return response