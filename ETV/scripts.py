from misc import Bot, customErrors, utils
from models import models
from FilterParamsInference import Inferencer
import sys

asciiout = False
asciiin = False
outfile = False
outpath = None

def create(name):
    return Bot.BotInstance(name).toJSON()


def trainModel(name,pathCorpus, rawKW, numIterations):
    if(numIterations is None):
        numIterations = utils.default_num_iterations
    try:
        utils.checkFile(pathCorpus)
        utils.checkAlphanumeric(rawKW, ",")
        utils.checkInt(numIterations)
    except FileNotFoundError as e:
        utils.error("Bad path" + " - " + str(e))
    except customErrors.InvalidCharsError as e:
        utils.error("Invalid param" + " - " + str(e))

    kw = rawKW.split(",")
    if(models.trainModel(pathCorpus, name, num_iterations=numIterations, _model_version=utils.default_model) != 0):
        utils.error("Error while training model")

    #descriptor de modelo
    return utils.modelDescriptor(name, kw)


def trainBot(jsonBot,model):
    bot = Bot.jsonConstructor(jsonBot)
    rawModel = utils.decModelDescriptor(model)
    try:
        utils.checkModelExists(rawModel["name"])
    except customErrors.BadParamError as e:
        utils.error("Error in model given: " + str(e))

    bot.learn(rawModel["name"],rawModel["keywords"])
    return bot.toJSON()

def getResponse(jsonBot,context, filterParams):
    bot = Bot.jsonConstructor(jsonBot)
    inferedParams = Inferencer.inferParams(bot,"dummy") #TODO
    finalParams = utils.fusionParams(filterParams,inferedParams)
    finalParams = utils.filterParams(finalParams.split(" "), 0)
    return bot.generateResponse(context,finalParams)

def setupBaseModel():
    utils.setupBaseModel()

def _main():
    v = sys.argv
    global asciiout
    global asciiin
    global outfile
    global outpath

    if("--ascii-out" in v):
        asciiout = True
        v.remove("--ascii-out")

    if ("--ascii-in" in v):
        asciiin = True
        v.remove("--ascii-in")

    if("--outfile" in v):
        outfile = True
        idx = v.index("--outfile")
        outpath = v[idx + 1]
        try:
            utils.checkFile(outpath)
        except FileNotFoundError as e:
            utils.error("Out file path not available : " + str(e))
        v.pop(idx)
        v.pop(idx)


    if(v[1] == "create"): #create name
        if(len(v) != 3):
            utils.error("Usage \"create name\"")
        ret = create(v[2])

    elif(v[1]=="trainModel"): #trainModel name pathCorpus "keywords,..." (-n int)
        if (len(v) < 5):
            utils.error("Usage \"trainModel name pathCorpus keywords,word,...\"")
        numIt = None
        if("-n" in v):
            numIt = v[v.index("-n") + 1]
        ret = trainModel(v[2],v[3],v[4], numIt)

    elif(v[1]=="trainBot"): #trainBot jsonBot modelDescriptor
        if (len(v) != 4):
            utils.error("Usage \"trainBot jsonBot modelDescriptor\"")
        jsonBot = v[2]
        jsonModel = v[3]
        if(asciiin):
            jsonBot = utils.asciiToText(v[2])
            jsonModel = utils.asciiToText(v[3])
        ret = trainBot(jsonBot,jsonModel)

    elif (v[1] == "getResponse"): #getResponse jsonBot context filterParams
        if (len(v) < 4):
            utils.error("Usage \"getResponse jsonBot \"context\" (filterParams, read filterParams file for more information)\"")
        filterParams = utils.filterParams(v, 4)
        jsonBot = v[2]
        if (asciiin):
            jsonBot = utils.asciiToText(v[2])
        return getResponse(jsonBot,v[3],filterParams)

    elif(v[1] == "setupBaseModel"):
        if(len(v) != 2):
            utils.error("Usage \"getResponse jsonBot \"context\" (filterParams, read filterParams file for more information)\"")
        setupBaseModel()
        exit(0)
    else:
        utils.error("Unknown command")

    if(asciiout):
        ret = utils.textToAscii(ret)

    if(outfile):
        with open(outpath, "w") as f:
            f.write(ret)
            exit(0)

    return ret


_main()