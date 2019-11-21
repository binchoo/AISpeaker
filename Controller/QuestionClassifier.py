#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
sys.path.append('../')
from speakerapp.question_classifier import getFinalResult

class QuestionClassifier:
    def classify(self, question):
        return getFinalResult('오늘 날씨 어때')