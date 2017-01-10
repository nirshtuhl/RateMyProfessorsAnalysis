import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

columns = [
    'department',
    'helpCount',
    'id',
    'name',
    'notHelpCount',
    'professorID',
    'rClarity',
    'rComments',
    'rDate',
    'rEasy',
    'rHelpful',
    'rInterest',
    'rOverall',
    'rStatus',
    'rWouldTakeAgain',
    'sId',
    'teacherGrade',
    'teacherRatingTags'
]

data = []
with open('RMPData.json', 'r') as file:
    reviews = json.load(file)
    for review in reviews:
        reviewToAdd = []
        for item in columns:
            reviewToAdd.append(review[item])
        data.append(reviewToAdd)

reviews = pd.DataFrame(data, columns=columns)

# overall rating counts
#plt.hist(reviews['rOverall'], bins=9)
#plt.show()


# overall difficulty counts
#plt.hist(reviews['rEasy'], bins=5)
#plt.show()


# comment length histogram
#lengths = reviews['rComments'].apply(lambda x: len(x))
#plt.hist(lengths, bins=10)
#plt.show()


# difficulty vs overall rating scatter
#ratingPairs = list(zip(reviews['rEasy'], reviews['rOverall']))
#s = set(ratingPairs)
#pairCounts = {}
#for pair in s:
#    pairCounts[pair] = ratingPairs.count(pair)
#
#difficulty = [i[0] for i in pairCounts.keys()]
#overall = [i[1] for i in pairCounts.keys()]
#sizes = [i * 3 for i in pairCounts.values()]
#
#fig = plt.figure()
#sub = fig.add_subplot(111)
#sub.scatter(difficulty, overall, s=sizes)
#plt.show()


# professor ratings scatter
# difficulty is x, overall is y
#reviewSummary = reviews[['name', 'rEasy', 'rOverall']].groupby(by='name').mean()
# unfortunately have to use existing column (in this case rEasy)
# to store review counts per professor, then rename it
#counts = reviews[['name', 'rEasy']].groupby(by='name').count()
#counts = counts.rename(columns = {'rEasy' : 'count'})
#plt.scatter(reviewSummary['rEasy'], reviewSummary['rOverall'], s=counts['count']*3)
#plt.show()


# grade received vs. reported difficulty
#withGrade = reviews[~reviews['teacherGrade'].isin(['N/A', 'Not sure yet', 'INC', 'WD'])]
#gradeMap = {'A+' : 4.0, 'A' : 4.0, 'A-' : 3.667, 'B+' : 3.333, 'B' : 3.0, 'B-' : 2.667, 'C+' : 2.333, 'C': 2.0, 'C-' : 1.667, 'D+' : 1.333, 'D' : 1.0, 'D-' : 0.667, 'F' : 0}
#withGrade = withGrade.replace({'teacherGrade' : gradeMap})
#
#gradePairs = list(zip(withGrade['teacherGrade'], withGrade['rEasy']))
#s = set(gradePairs)
#pairCounts = {}
#for pair in s:
#    pairCounts[pair] = gradePairs.count(pair)
#
#grade = [i[0] for i in pairCounts.keys()]
#overall = [i[1] for i in pairCounts.keys()]
#sizes = [i * 7 for i in pairCounts.values()]
#
#m, b = np.polyfit(withGrade['teacherGrade'], withGrade['rEasy'], 1)
#yHat = m * withGrade['teacherGrade'] + b
#yBar = withGrade['rEasy'].mean()
#SSReg = sum((yHat - yBar)**2)
#SSTot = sum((withGrade['rEasy'] - yBar)**2)
#rSquared = SSReg / SSTot
#print(rSquared)
#
#plt.scatter(grade, overall, s=sizes)
#plt.plot(withGrade['teacherGrade'], m*withGrade['teacherGrade'] + b, '-')
#plt.show()
