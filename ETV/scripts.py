import Bot
import models
import utils
import customErrors
import sys


def create(name):
    return Bot.BotInstance(name).toJSON()

def trainModel(name,pathCorpus, rawKW):
    try:
        utils.checkFile(pathCorpus)
        utils.checkAlphanumeric(rawKW,",")
    except FileNotFoundError:
        utils.error("Bad path")
    except customErrors.InvalidCharsError:
        utils.error("Invalid keywords")


    kw = rawKW.split(",")
    if(models.trainModel(pathCorpus, name) != 0):
        utils.error("dummy")

    #descriptor de modelo
    return utils.modelDescriptor(name,kw)


def trainBot(jsonBot,model):
    bot = Bot.jsonConstructor(jsonBot)
    rawModel = utils.decModelDescriptor(model)
    bot.learn(rawModel["name"],rawModel["keywords"])
    return bot.toJSON()

def getResponse(jsonBot,context, *filterParams):
    bot = Bot.jsonConstructor(jsonBot)
    bot.generateResponse(context) #TODO filterparams

def _main():
    v = sys.argv

    if(v[1] == "create"): #create name
        if(len(v) != 3):
            utils.error("dummy")
        return create(v[2])

    elif(v[1]=="trainModel"): #trainModel name pathCorpus "keywords,..."
        if (len(v) != 5):
            utils.error("dummy")
        return trainModel(v[2],v[3],v[4])

    elif(v[1]=="trainBot"): #trainBot jsonBot model
        if (len(v) != 4):
            utils.error("dummy")
        return trainBot(v[2],v[3])

    elif (v[1] == "getResponse"): #getResponse jsonBot context filterParams
        if (len(v) != 4): #TODO filterparams
            utils.error("dummy")
        filterParams = utils.filterParams(v,4)
        return getResponse(v[2],v[3],filterParams)
    else:
        utils.error("dummy")

    exit(0)

_main()