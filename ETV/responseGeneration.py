

def generateResponse(model, seed, nwords = 20):
    result = model.generate(num_words=nwords, text_seed=seed)
    return _detokenize(result)

def generateText(model, nwords = 20):
    result = model.generate(num_words=nwords)
    return _detokenize(result)
