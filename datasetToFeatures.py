from flaskServer.featureExtraction import url_to_features, generate_brandlist
import csv
from progress.bar import IncrementalBar


#-------------------------------------------- Feature Files ------------------------------------------------------------------------
#Used to specify the name of the dataset file and the name of the resulting feature file.
readFile = r"datasets/KaggleDataset.csv"
writeFile = r"featureFiles/Kaggle_features.csv"

#-----------------------------------------------------------------------------------------------------------------------------------


if __name__=="__main__":
    file_len = 0
    brandlist = generate_brandlist()

    for i in open(readFile, encoding='utf8'):
        file_len = file_len + 1

    #Creates a progress bar to show how many lines have been converted to features for the given file
    bar = IncrementalBar("progress", max=file_len)

    #Opens the file "readFile", for each line runs the url_to_features function and writes the features to the "writefile" file.
    with open(readFile, encoding='utf8', newline="") as newfile:
        with open(writeFile, "w") as write:
            reader = csv.reader(newfile, delimiter=',', quotechar='|')
            writer = csv.writer(write, delimiter=",", lineterminator="\n")
            next(reader)
            for row in reader:    
                features = url_to_features(row[0], brandlist)
                features.append(row[1])
                writer.writerow(features)
                bar.next()
            
        bar.finish()
        write.close()
    newfile.close()