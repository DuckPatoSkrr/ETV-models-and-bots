import Bot
#IGNORAR MAIN, AHORA MISMO ES SOLO PARA EL TESTEO

# MAIN
def main():
    myBot = Bot.BotInstance("jerry")
    print(myBot.name)
    corpus = ""
    f = open("input", "r", encoding = "utf8")
    for i in f:
        corpus += i

    myBot.learn(corpus, "Trump")
    print(myBot.mymodelsnames)
    print(myBot.generateText("Trump"))
    exit(0)

    
if __name__ == "__main__":
    main()