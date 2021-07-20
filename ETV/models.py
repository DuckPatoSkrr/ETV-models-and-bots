import os
import gpt_2_simple as gpt2
import utils
# PRIVATE

#PUBLIC

#corpus must be a txt
def trainModel(corpusPath, nameOfModel, num_iterations = 5, _model_version = "124M"): #124M o 355M
    if not os.path.isdir(os.path.join("models", _model_version)):
        print(f"Downloading {_model_version} model...")
        gpt2.download_gpt2(model_name=_model_version, model_dir="models")  # model is saved into current directory under /(model_dir)/(model_name)/

    utils.checkFile(corpusPath)

    sess = gpt2.start_tf_sess() #config (threads and external server)
    gpt2.finetune(sess, corpusPath,
                  model_name=_model_version, steps=num_iterations, run_name=nameOfModel,
                  restore_from='fresh', multi_gpu=False,)  # steps is max number of training step

    return 0



