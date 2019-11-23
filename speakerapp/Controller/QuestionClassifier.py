#!/usr/bin/python
# -*- coding: utf-8 -*-

from speakerapp import question_classifier


class QuestionClassifier:
    def __init__(self):
        pass

    def classify(self, question):
        return question_classifier.getFinalResult(question)
