import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.


    """
    labels=[]
    evidence=[]
    with open(f"{filename}", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        i=0

        for row in reader:
            i+=1
            evi_dict=row.values()
            label_list=[]
            evi_list=list(evi_dict)
            for k in [0,2,4,11,12,13,14]:
                evi_list[k]=int(evi_list[k])
            for j in [1,3,5,6,7,8,9]:
                evi_list[j]=float(evi_list[j])
                
                

            if evi_list[10]=="Jan":
               evi_list[10]=0
            elif evi_list[10]=="Feb":
               evi_list[10]=1
            elif evi_list[10]=="Mar":
               evi_list[10]=2    
            elif evi_list[10]=="Apr":
               evi_list[10]=3
            elif evi_list[10]=="May":
               evi_list[10]=4
            elif evi_list[10]=="June":
               evi_list[10]=5
            elif evi_list[10]=="Jul":
               evi_list[10]=6
            elif evi_list[10]=="Aug":
               evi_list[10]=7    
            elif evi_list[10]=="Sep":
               evi_list[10]=8
            elif evi_list[10]=="Oct":
               evi_list[10]=9
            elif evi_list[10]=="Nov":
               evi_list[10]=10
            elif evi_list[10]=="Dec":
               evi_list[10]=11

            


            if evi_list[15]=="Returning_Visitor":
               evi_list[15]=1
            else:
                evi_list[15]=0

            if evi_list[16]=="TRUE":
               evi_list[16]=1
            else:
                evi_list[16]=0

            if evi_list[17]=="TRUE":
               evi_list[17]=1
            else:
                evi_list[17]=0
            label_list.append(evi_list[17])
            evi_list.pop(17) 
            evidence.append(evi_list)
            labels.extend(label_list)         
     
     
    result=[evidence,labels]
    

    return tuple(result)
    


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(evidence, labels)
    
    return neigh
    


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.


  """
    a=b=c=d=0
    for i in range(len(labels)):
        if labels[i]==1:
            a+=1 #total no. of labels which are marked positive
        else:
            c+=1 #total no. of labels which are marked negative
        if labels[i]==1 and predictions[i]==1:
            b+=1 
        elif labels[i]==0 and predictions[i]==0:
            d+=1 
    
  #  print(a,b,c,d)
    sens=b/a
    spec=d/c

    return(sens,spec)

          
  


if __name__ == "__main__":
    main()
