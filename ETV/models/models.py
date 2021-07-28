import os
import gpt_2_simple as gpt2
from misc import utils

models_dir = "models"
default_model_version = "124M"

# PRIVATE

#PUBLIC

#corpus must be a txt
def trainModel(corpusPath, nameOfModel, num_iterations = 5, _model_version = default_model_version): #124M o 355M
    if not os.path.isdir(os.path.join(models_dir, _model_version)):
        utils.error("Model introduced does not exist")

    utils.checkFile(corpusPath)

    sess = gpt2.start_tf_sess() #config (threads and external server)
    gpt2.finetune(sess, corpusPath,
                  model_name=_model_version, steps=num_iterations, run_name=nameOfModel,
                  restore_from='fresh', multi_gpu=False,)  # steps is max number of training step

    return 0



