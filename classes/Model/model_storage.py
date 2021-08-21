
import torch
import pickle



def saveModel(model, name="Default"):

    # create a dictionary to save all model information
    model_dict = {}
    
    # save model name
    model_dict['name'] = name

    # save model class
    model_dict['class'] = model

    # save model state_dict
    model_dict['state_dict'] = model.state_dict()

    # save optimizer state_dict

    # save model dict to pickle file
    with open('./saved_models/'+name+'.pickle', 'wb') as handle:
        pickle.dump(model_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def loadModel(model_name):

    with open('./saved_models/'+model_name+'.pickle', 'rb') as handle:
        model = pickle.load(handle)

    return model







