import responseGeneration
import models
import json

class BotInstance:

    #PRIVATE

    def _getModelBasedOnMood(self, mood):
        #TODO puede que utilizando keywords sea una buena manera
        return self.mymodelsnames[0]


    name = "noname"
    mymodelsnames = []

    #PUBLIC

    def __init__(self, name, loadModels=[]):
        self.name = name
        self.mymodelsnames = loadModels




    def generateResponse(self, myMood, positivityFactor,
                         prefix=None):
        model = self._getModelBasedOnMood(myMood)
        return responseGeneration.generateResponse(model, positivityFactor, prefix)


    def learn(self, corpusPath, nameOfMood):
        models.trainModel(corpusPath,nameOfMood)
        self.mymodelsnames.append(nameOfMood)

    def toJSON(self):
        jsonFile = {"name":self.name,"mymodelsnames":self.mymodelsnames}
        return json.dumps(jsonFile)

def jsonConstructor(input):
    out = json.loads(input)
    name = out["name"]
    modelsList = out["mymodelsnames"]
    return BotInstance(name,modelsList)