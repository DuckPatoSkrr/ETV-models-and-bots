import responseGeneration

import models


class Bot:

    name = "noname"
    mymodels = []
    mymodelsnames = []

    def __init__(self, name):
        self.name = name

    def generateResponse(self, input, myMood):
        model = _getModelBasedOnMood(myMood)
        return responseGeneration.generateResponse(model, input)

    def generateText(self, myMood):
        model = getModelBasedOnMood(myMood)
        return responseGeneration.generateText(model)

    def learn(self, corpus, nameOfMood):
        mymodels.append(models.trainModel(corpus))
        mymodelsnames.append(nameOfMood)

    #PRIVATE

    def _getModelBasedOnMood(self, mood):
        #TODO
        pass