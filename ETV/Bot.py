import responseGeneration

import models


class BotInstance:

    name = "noname"
    _mymodels = []
    mymodelsnames = []

    def __init__(self, name):
        self.name = name

    def generateResponse(self, input, myMood):
        model = _getModelBasedOnMood(myMood)
        return responseGeneration.generateResponse(model, input)

    def generateText(self, myMood):
        model = self._getModelBasedOnMood(myMood)
        return responseGeneration.generateText(model)

    def learn(self, corpus, nameOfMood):
        self._mymodels.append(models.trainModel(corpus))
        self.mymodelsnames.append(nameOfMood)

    #PRIVATE

    def _getModelBasedOnMood(self, mood):
        #TODO
        return self._mymodels[0]