import Bot
#from gpt_2_finetuning import download_model
#IGNORAR MAIN, AHORA MISMO ES SOLO PARA EL TESTEO

# MAIN
def main():
    #download_model

    tom = Bot.BotInstance("tom");
    tom.learn("testDataset.csv", "test")

    exit(0)

    
if __name__ == "__main__":
    main()