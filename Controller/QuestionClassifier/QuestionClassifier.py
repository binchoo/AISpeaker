#!/usr/bin/python
#-*- coding: utf-8 -*-
from speakerapp import question_classifier

class QuestionClassifier:

    def classify(self, question):
        return question_classifier.getFinalResult(question)
