from transformers import GPT2Tokenizer
from transformers import GPT2Model
from transformers import TrainingArguments
from transformers import Trainer
from datasets import load_dataset


#raw_datasets = load_dataset("imdb")


# PRIVATE

#loads dataset from csv file
def _prepareDatasets(input):
    return load_dataset( 'csv', data_files=input)


#PUBLIC


#la entrada es un csv, la columna llamada data es la que debe contener los textos que se utilizaran
def trainModel(corpusTrainPath, corpusEvalPath):
    # formateo los csv a datasets
    rawtrainset = _prepareDatasets(corpusTrainPath)
    rawevalset = _prepareDatasets(corpusEvalPath)

    #tokenizamos
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenTrain = tokenizer(rawtrainset["train"]["data"])
    tokenEval = tokenizer(rawevalset["train"]["data"])


    #preparamos el modelo
    model = GPT2Model.from_pretrained("gpt2")
    training_args = TrainingArguments("test_trainer") #directorio para guardar checkpoints

    #le proporcionamos al trainer el modelo con su configuracion, y el set de training y el de evaluacion
    trainer = Trainer(
        model=model, args=training_args, train_dataset=tokenTrain, eval_dataset=tokenEval
    )

    trainer.train()
    return model


