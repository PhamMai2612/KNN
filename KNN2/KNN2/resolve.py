
from __future__ import print_function
import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory.'+ directory)

with open('articles.json',encoding="utf8") as json_data:
    articles = json.load(json_data)
    print(len(articles), "Articles loaded successfully")

    list_of_type = {}

    for article in articles:
        types = article['type']
        createFolder('./'+types+'/')

        title = ''
        for headline in  article['headline']:
            title = title +" "+ headline
        content = ''

        if types not in list_of_type:

            list_of_type[types] = 0
        else:
            list_of_type[types] = list_of_type[types] + 1

        for paragraph in article['content']:
            content = content + " " +paragraph
        # print(content)

        completeName = os.path.join('./'+types+'/', str(list_of_type[types]) +'.txt')
        file = open(completeName, "w", encoding="utf8")
        file.write(title+ " "+content)

label = 0
total_filelist = []
total_label = []
for cate in list_of_type.keys():
    file_list = ["./"+cate+"/" + str(i)+".txt" for i in range(0,list_of_type[cate]+1)]
    for i in range(0, list_of_type[cate]+1):
        total_label.append(label)
    label += 1
    total_filelist.extend(file_list)

X = TfidfVectorizer(input= "filename").fit_transform(total_filelist).toarray()


neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X, total_label)

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, total_label_train, total_label_test = train_test_split(X, total_label, test_size = 0.25, random_state=0)


# Predicting the Test set results
total_label_pred = neigh.predict(X_test)

# Accuracy
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(total_label_test, total_label_pred) * 100
print(accuracy)
