import numpy as np
import pickle
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

#------------------------------------- Model ---------------------------------------------------------------------------------------
model_file = r"pickledModels/RF_DatasetA.sav"
#------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------- Feature Files ------------------------------------------------------------------------
featureFile = r"featureFiles/Kaggle_features.csv"
#-----------------------------------------------------------------------------------------------------------------------------------

if __name__=="__main__":
    #Loads the model from the pickle file specified in model_file
    model = pickle.load(open(model_file, "rb"))
    print("model created")

    #Generates a numpy array from the file "featureFile"
    new_feats = np.genfromtxt(featureFile, delimiter=",", dtype=np.int32)

    #Seperates the array into the samples and targets
    samples = new_feats[:,:-1]
    targets = new_feats[:,-1]

    #Makes predcitons on the given samples
    predictions = model.predict(samples)


    #The print statements are used to review accuracy, f1-score and precision of the models. 
    print(model)
    print("Accuracy: {acc}".format(acc=accuracy_score(targets, predictions)))
    print("Precision: {prec}".format(prec= precision_score(targets, predictions)))
    print("Recall: {rec}".format(rec=recall_score(targets, predictions)))
    print("F-Score: {f1}".format(f1=f1_score(targets, predictions)))