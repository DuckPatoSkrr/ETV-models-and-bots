from nltk.lm import MLE
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk import word_tokenize, sent_tokenize

NGRAM_MAX = 2

testCorpus = "yo opino que mariano rajoy es un makinon"

def testModel():
    return trainModel("test", testCorpus)

def getModel(usertype):
    return testModel()

def trainModel(usertype, corpus):
    tokenized_text = [list(map(str.lower, word_tokenize(sent)))
                      for sent in sent_tokenize(corpus)]

    train_data, padded_sents = padded_everygram_pipeline(NGRAM_MAX, tokenized_text)

    model = MLE(NGRAM_MAX)
    model.fit(train_data, padded_sents)

    storeModel(model, usertype)
    return model

def storeModel(model,usertype):
    pass
    #database.storemodel(key = usertype, value = model)