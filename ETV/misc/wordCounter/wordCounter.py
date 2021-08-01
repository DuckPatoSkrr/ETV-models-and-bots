import os

def counter(inpath,outpath, n):
    cwd = os.getcwd()
    os.chdir("./misc/wordCounter")
    os.system(f"wordCounter.exe {inpath} {outpath} {n}")
    os.chdir(cwd)
