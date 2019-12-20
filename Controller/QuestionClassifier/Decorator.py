from .QuestionClassifier import IClassifier
import re

class Decorator(IClassifier) :

    def __init__(self, base) :
        self.base = base

    def classify(self, question) :
        q_type = self.base.classify(question)
        return self._classify(question, q_type)

    def _classify(self, question, base_q_type) :
        pass

class RNNClassifier_V2(Decorator) :
    
    def _classify(self, question, base_q_type) :
        
        if base_q_type == 'weather' :
            pass
        else :
            return base_q_type

class RegexClassifier_V2(Decorator) :
    
    def _classify(self, question, base_q_type) :

        if base_q_type == 'weather' :
            regex_dict = { 
                'uv' : re.compile(r'오존'),
                'finedust': re.compile(r'미세먼지'), 
                'rain' : re.compile(r'비|눈|우산'),
            }
            for sub_type in regex_dict :
                regex = regex_dict[sub_type]
                if regex.search(question) != None :
                    return sub_type
        return base_q_type