from misc import Bot


# MAIN
def main():
    test = Bot.BotInstance("test", loadModels=["testMood"], modelKeywords={"testMood":["key1", "key2"]})
    json = test.toJSON()
    otroTest = Bot.jsonConstructor(json)
    print(otroTest.toJSON())

    exit(0)

    
if __name__ == "__main__":
    main()