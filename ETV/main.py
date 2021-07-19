import Bot
import sentimentAnalysis
# MAIN
def main():
    test = Bot.BotInstance("test",loadModels=["testMood"])
    test.generateResponse("dummy")
    exit(0)

    
if __name__ == "__main__":
    main()