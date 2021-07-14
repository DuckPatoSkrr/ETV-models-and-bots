from transformers import AutoTokenizer
from transformers import AutoModel #TODO elegir el modelo de textGeneration
from transformers import TrainingArguments
from transformers import Trainer
from torch.utils.data import Dataset, DataLoader
from datasets import load_dataset

#raw_datasets = load_dataset("imdb")


# PRIVATE

def _prepareDatasets(input):
    return dataset


#PUBLIC


#debo definir bien el formato de entrada el corpus TODO
def trainModel(corpusTrain, corpusEval):
    #tokenizamos el corpus
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    trainTokens = tokenizer(corpusTrain)
    evalTokens = tokenizer(corpusEval)

    #formateo los datasets para poder meterlos en el trainer
    trainset = _prepareDatasets(trainTokens)
    evalset = _prepareDatasets(evalTokens)

    #preparamos el modelo
    model = AutoModelForSequenceClassification.from_pretrained("gpt2") #TODO
    training_args = TrainingArguments("test_trainer") #directorio para guardar checkpoints

    #le proporcionamos al trainer el modelo con su configuracion, y el set de training y el de evaluacion
    trainer = Trainer(
        model=model, args=training_args, train_dataset=trainset, eval_dataset=evalset
    )

    trainer.train()
    return model


