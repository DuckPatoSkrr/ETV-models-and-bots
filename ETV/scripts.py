from misc import Bot, customErrors, utils
from models import models
import sys

asciiout = False
asciiin = False
outfile = False
outpath = None

def create(age,level_of_education,likes,dislikes):
    try:
        utils.checkInt(age)
        utils.checkInt(level_of_education)
        utils.checkAlphanumeric(likes,',',' ')
        utils.checkAlphanumeric(dislikes, ',',' ')
    except customErrors.InvalidCharsError as e:
        utils.error(f"Error while creating bot, bad param: {str(e)}")
    splikes = likes.split(",")
    spdislikes = dislikes.split(",")
    for i in range(len(splikes)):
        splikes[i] = utils.unifyWord(splikes[i])
    for i in range(len(spdislikes)):
        spdislikes[i] = utils.unifyWord(spdislikes[i])

    return Bot.BotInstance(age,level_of_education,likes=splikes,dislikes=spdislikes).toJSON()


def trainModel(name,pathCorpus, mdl, numIterations):
    if(numIterations is None):
        numIterations = utils.default_num_iterations
    pathCorpus = f"{models.corpus_dir}{pathCorpus}"
    try:
        utils.checkFile(pathCorpus)
        utils.checkInt(numIterations)
        numIterations = int(numIterations)
    except FileNotFoundError as e:
        utils.error("Bad path" + " - " + str(e))
    except customErrors.InvalidCharsError as e:
        utils.error("Invalid param" + " - " + str(e))

    mdl = models.getModelDescriptorListObj(mdl)
    ret = models.appendModelDescriptorList(mdl, models.Model(name, pathCorpus,numIterations))
    #descriptor de modelo
    return models.modelDescriptorListToJSON(ret)


def trainBot(jsonBot,modelDescriptorList):
    bot = Bot.jsonConstructor(jsonBot)
    modelList = models.getModelDescriptorListObj(modelDescriptorList)
    bot.learn(modelList)
    return bot.toJSON()

def getResponse(jsonBot,context, filterParams):
    bot = Bot.jsonConstructor(jsonBot)
    return bot.generateResponse(context,filterParams)

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

        v.pop(idx)
        v.pop(idx)


    if(v[1] == "create"): #create age level_of_education "likes" "dislikes"
        if(len(v) != 6):
            utils.error("Usage \"create age level_of_education \"likes\" \"dislikes\" \"")
        ret = create(v[2],v[3],v[4],v[5])

    elif(v[1]=="trainModel"): #trainModel name pathCorpus "keywords,..." (-n int)
        if (len(v) < 5):
            utils.error("Usage \"trainModel name pathCorpus \"modelDescriptorList\" (-n numIterations)\"")
        numIt = None
        if("-n" in v):
            numIt = v[v.index("-n") + 1]
        ret = trainModel(v[2],v[3],v[4], numIt)

    elif(v[1]=="trainBot"): #trainBot jsonBot modelDescriptorList
        if (len(v) != 4):
            utils.error("Usage \"trainBot jsonBot modelDescriptorList\"")
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
        ret = getResponse(jsonBot,v[3],filterParams)

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


print(_main())