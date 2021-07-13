from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.lm import MLE
import models

def _detokenize(result):
    detokenizer = TreebankWordDetokenizer().detokenize
    content = []
    for token in result:
        if token == '<s>':
            continue
        if token == '</s>':
            break
        content.append(token)
    return detokenizer(content)


def getResponse(model, seed, nwords = 20):
    result = model.generate(num_words=nwords, text_seed=seed)
    return _detokenize(result)
