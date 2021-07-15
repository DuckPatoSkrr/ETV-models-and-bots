#import responseGeneration
import models


class BotInstance:


    #PRIVATE

    def _getModelBasedOnMood(self, mood):
        #TODO
        return self._mymodels[0]


    name = "noname"
    _mymodels = []
    mymodelsnames = []

    #PUBLIC

    def __init__(self, name):
        self.name = name

    def generateResponse(self, input, myMood):
        model = self._getModelBasedOnMood(myMood)
        return responseGeneration.generateResponse(model, input)

    def generateText(self, myMood):
        model = self._getModelBasedOnMood(myMood)
        return responseGeneration.generateText(model)

    def learn(self, corpus, nameOfMood):
        #splitCorpus(corpus, train, test)
        self._mymodels.append(models.trainModel(corpus, corpus))
        self.mymodelsnames.append(nameOfMood)
