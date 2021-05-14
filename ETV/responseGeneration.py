from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.lm import MLE

import models
def detokenize(result):
    detokenizer = TreebankWordDetokenizer().detokenize
    content = []
    for token in result:
        if token == '<s>':
            continue
        if token == '</s>':
            break
        content.append(token)
    return detokenizer(content)


def getTextSeed(msgtype):
    return "yo opino"
    #databas.getTextSeed(msgtype)


def getResponse(usertype, msgtype, nwords = 20):

    textSeed = getTextSeed(msgtype)
    model = models.getModel(usertype)
    result = model.generate(num_words=20, text_seed=textSeed)

    return (detokenize(result))
