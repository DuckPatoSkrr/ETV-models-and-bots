import Bot
#IGNORAR MAIN, AHORA MISMO ES SOLO PARA EL TESTEO

# MAIN
def main():
    myBot = Bot.BotInstance("jerry")
    print(myBot.name)
    myBot.learn("testDataset.csv", "Test")
    print(myBot.mymodelsnames)
    exit(0)

    
if __name__ == "__main__":
    main()