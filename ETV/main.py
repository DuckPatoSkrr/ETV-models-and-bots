from misc.wordCounter import wordCounter
import threading
import os
import time
from models import models
# MAIN


def main():
    print(models._generateKeywords("shakespeare.txt"))

    exit(0)

    
if __name__ == "__main__":
    main()