from .IClassifier import IClassifier

class Decorator(IClassifier) :

    def __init__(self, base) :
        self.base = base

    def classify(self, question) :
        q_type = self.base.classify(question)
        return self._classify(question, q_type)

    def _classify(self, question, base_q_type) :
        pass

import re
class SpecificRegexClassifier(Decorator) :
    
    def _classify(self, question, base_q_type) :

        if base_q_type == 'weather' :
            regex_dict = { 
                'ozon' : re.compile(r'오존'),
                'finedust': re.compile(r'미세먼지'), 
                'rain' : re.compile(r'비|눈|우산'),
                'temperature' : re.compile(r'기온|온도'),
            }
        elif base_q_type == 'bible' :
            regex_dict = {
                'todaybible' : re.compile(r'오늘')
            }
        else :
            return base_q_type

        for sub_type in regex_dict : 
            regex = regex_dict[sub_type]
            if regex.search(question) != None :
                return sub_type
        return base_q_type

class SpecificRNNClassifier(SpecificRegexClassifier) :
    pass