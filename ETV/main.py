import Bot
#IGNORAR MAIN, AHORA MISMO ES SOLO PARA EL TESTEO

testCorpus = ["Hello my name is Ventura  and my dick is big.", "My peepee dont fit in my poopoo"]

# MAIN
def main():
    myBot = Bot.BotInstance("jerry")
    print(myBot.name)
    myBot.learn(testCorpus, "Test")
    print(myBot.mymodelsnames)
    exit(0)

    
if __name__ == "__main__":
    main()