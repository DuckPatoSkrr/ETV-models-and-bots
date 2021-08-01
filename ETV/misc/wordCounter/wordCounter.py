import sys,os

def counter(inpath,outpath, n):
    os.system(f"./misc/wordCounter/wordCounter.exe {inpath} {outpath} {n}")