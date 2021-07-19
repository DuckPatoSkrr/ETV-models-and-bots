import gpt_2_simple as gpt2
import sentimentAnalysis

default_max_output = 500
default_number_of_responses = 10
default_max_words = 300

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
    classifier = sentimentAnalysis.Classifier()

    for duple in input:
        prop = classifier.classify(duple[0])
        duple[1] += 10 - (abs(posFactor - prop.sentiment_polarity) * 5)


def _pipeFormat(input,nchars): #format text, this doesn't change the puntuation

    for duple in input:
        output = ""
        splitedInput = duple[0].split(".")
        i = 0
        while (len(output) + len(splitedInput[i]) < nchars and i < len(splitedInput)):
            output += splitedInput[i] + "."
            i += 1

        output.replace("\n\n", "\n")
        duple[0] = output

    return input

def _processedText(input, nchars,positivityFactor): #filters the output of the model TODO
    output = _duple(input)
    output = _pipeFormat(output,nchars)
    output = _pipePositivity(output,positivityFactor)
    return _maxPoints(output)


def generateResponse(model, prefix = None, nchars = default_max_output, number_of_responses = default_number_of_responses):
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name=model)
    textGenerated = gpt2.generate(sess, prefix=prefix, run_name=model,
                                  batch_size=number_of_responses, nsamples=number_of_responses,
                                  return_as_list=True, length=default_max_words)
    return _processedText(textGenerated,nchars)



