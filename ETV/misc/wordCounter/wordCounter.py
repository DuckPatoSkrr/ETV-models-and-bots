import os
import string
import spacy

def counter(inpath,outpath, n):
    cwd = os.getcwd()
    os.chdir("./misc/wordCounter")
    os.system(f"wordCounter.exe {inpath} {outpath} {n}")
    os.chdir(cwd)

def tokenize(inpath, outpath):
    cachedStopWords = spacy.load('en_core_web_sm').Defaults.stop_words
    for w in string.punctuation:
        cachedStopWords.add(w)
    loadChunk = lambda f: ' '.join(f.readlines(1024))
    outf = open(outpath, "w", errors="ignore")
    translator = str.maketrans('', '', string.punctuation)

    with open(inpath,"r") as file:
        chunk = loadChunk(file)
        while chunk:
            text = chunk.lower()
            text = text.translate(translator)
            text = ' '.join([word for word in text.split() if word not in cachedStopWords])
            outf.write(text)

            chunk = loadChunk(file)
