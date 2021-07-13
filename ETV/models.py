from nltk.lm import MLE
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk import word_tokenize, sent_tokenize

NGRAM_MAX = 3

def trainModel(corpus):
    tokenized_text = [list(map(str.lower, word_tokenize(sent)))
                      for sent in sent_tokenize(corpus)]

    train_data, padded_sents = padded_everygram_pipeline(NGRAM_MAX, tokenized_text)

    model = MLE(NGRAM_MAX)
    model.fit(train_data, padded_sents)

    return model

