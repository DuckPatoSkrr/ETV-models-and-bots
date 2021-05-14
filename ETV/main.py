import sentimentAnalysis
import responseGeneration
import sys

# MAIN
def main():
    args = sys.argv

    if args[1] == "-help":
        print("Usage: ")
    elif args[1] == "analyze":
        sentimentAnalysis.analize()
    elif args[1] == "response":
        responseGeneration.getResponse("test","test","test")
    else:
        print("Error")
    exit(0)

    
if __name__ == "__main__":
    main()