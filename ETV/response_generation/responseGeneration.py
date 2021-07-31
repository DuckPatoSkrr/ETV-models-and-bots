import gpt_2_simple as gpt2
from sentiment_analysis import sentimentAnalysis

def _maxPoints(list):
    max = list[0]
    for i in list:
        if i[1] > max[1]:
            max = i

    return max[0]

def _duple(input): #transform a list of str to a list of duples [("text",0),...]
    output = []
    for i in input:
        output.append((i,0))
    return output

def _pipePositivity(input, posFactor):
    if(posFactor is None):
        return input
    classifier = sentimentAnalysis.Classifier()
    outList =[]
    for duple in input:
        prop = classifier.classify(duple[0])
        res = 10 - (abs(posFactor - prop.sentiment_polarity) * 5)
        outList.append((duple[0],duple[1] + res))

    return outList

def _pipeFormat(input,nchars): #format text, this doesn't change the puntuation
    if(nchars == -1):
        return input
    outList = []
    for duple in input:
        output = ""
        splitedInput = duple[0].split(".")
        i = 0
        while (len(output) + len(splitedInput[i]) < nchars and i < len(splitedInput)):
            output += splitedInput[i] + "."
            i += 1

        output = output.replace("\n\n", "\n")
        outList.append((output,duple[1]))

    return outList

def _pipeKeywords(input, keywords): #gives points for each keyword that appears. Amount of each keyword does NOT matter, better for short texts
    if len(keywords) == 0:
        return input

    outList = []
    for duple in input:
        appearances = 0
        for word in keywords:
            if duple[0].find(word) > -1:
                appearances += 1
        score = (appearances * 10) / len(keywords)
        outList.append((duple[0], duple[1] + score))
    return outList

def _pipeKeywordCount(input, keywords): #gives points the more times keywords appear. Repeated keywords also add points. Can be useful for long texts
    if len(keywords) == 0:
        return input

    outList = []
    auxList = []
    maxScore = 0
    for duple in input:
        appearances = 0
        text_array = duple[0].split
        for word in keywords:
            appearances += text_array.count(word)
        if appearances > maxScore:
            maxScore = appearances
        auxList.append((duple[0], duple[1], appearances))
    for aux in auxList:
        score = (aux[2] * 10) / maxScore
        outList.append((aux[0], aux[1] + score))
    return outList

def _processedText(input, nchars,positivityFactor, keywords): #filters the output of the model
    output = _duple(input)
    output = _pipeFormat(output,nchars)
    output = _pipePositivity(output,positivityFactor)
    output = _pipeKeywordCount(output, keywords)
    return _maxPoints(output)


def generateResponse(model,
                     posFactor,
                     keyWords,
                     nchars,
                     number_of_responses,
                     prefix = None):
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name=model.name)
    textGenerated = gpt2.generate(sess, prefix=prefix, run_name=model.name,
                                  batch_size=number_of_responses, nsamples=number_of_responses,
                                  return_as_list=True, length=nchars)
    return _processedText(textGenerated,nchars, posFactor, keyWords)




