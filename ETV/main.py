#import sentimentAnalysis
import responseGeneration

#IGNORAR MAIN, AHORA MISMO ES SOLO PARA EL TESTEO

# MAIN
def main():
    response = responseGeneration.getResponse("dummy","dummy")
    print(response)
    exit(0)

    
if __name__ == "__main__":
    main()