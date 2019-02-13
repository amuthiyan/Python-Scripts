import numpy as np
import pandas as pd

from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import accuracy_score, classification_report,confusion_matrix
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

#Necessary Functions
#Sorting Family Size
def sepFamilySize(x):
    if x<=3:
        return 'small'
    else:
        return 'large'

#Sorting Occupation Types
def sepOccupationTypes(x):
    low_skill = ['Laborers','Low-skill Laborers','Security staff','Drivers']
    service = ['Cooking staff','Cleaning staff','Private service staff','Waiters/barmen staff','Realty agents']
    skill_staff = ['Sales staff','Core staff','Managers','High skill tech staff','Accountants','Medicine staff',\
                  'HR staff','IT staff']

    if x in low_skill:
        return "Unskilled"
    if x in service:
        return "Service Industry"
    if x in skill_staff:
        return "Skilled"
    if x == 'NaN':
        return 'Unemployed'

#Sorting Organization Types
def cleanOrgTypes(x):
    if ':' in x:
        x = x.split(': ')
        x = x[0]

    if 'Business' in x:
        x = 'Business Entity'

    edu = ['School','Kindergarten','University']
    if x in edu:
        x = 'Education'

    real_estate = ['Realtor','Housing']
    if x in real_estate:
        x = 'Real Estate'

    hosp = ['Hotel','Restaurant','Cleaning']
    if x in hosp:
        x = 'Hospitality'

    security = ['Security','Security Ministries']
    if x in security:
        x = 'Security'

    if x == 'XNA':
        x = "Unemployed"

    fin = ['Bank','Insurance']
    if x in fin:
        x = 'Finance'

    other = ['Electricity','Insurance','Telecom','Emergency','Advertising','Culture','Mobile',\
            'Legal Services','Religion']
    if x in other:
        x = 'Other'

    return x

#Sort House Ownership
def ownHouse(x):
    if x == 'House / apartment':
        return 'Yes'
    else:
        return 'No'

#Sort Income Categories
def sortIncomeType(x):
    not_working = ['Pensioner','Unemployed','Student','Maternity leave']
    if x in not_working:
        return 'Not Working'
    elif x == 'Businessman':
        return 'Working'
    else:
        return x

#Sort Marital Status
def sortMarriedStatus(x):
    marry = ['Married','Civil marriage']
    if x in marry:
        return 'Married'
    else:
        return 'Not Married'

#Importing the dataset
df = pd.read_csv("Bank_Loan_Data.csv")

#Feature Engineering Phase
df['Family_Size'] = df.cnt_fam_members.apply(sepFamilySize)

df['Job_Types'] = df.occupation_type.apply(sepOccupationTypes)
df['Job_Types'] = df.Job_Types.fillna('Unemployed')

df['organization_type'] = df.organization_type.apply(cleanOrgTypes)

df['Owns_House'] = df.name_housing_type.apply(ownHouse)

df['Income_Cats'] = df.name_income_type.apply(sortIncomeType)

df['Married_Flag'] = df.name_family_status.apply(sortMarriedStatus)

#Model Building Phase
#Define features to use
features = ['code_gender','flag_own_car', 'flag_own_realty','organization_type', 'Family_Size', 'Job_Types',\
            'Owns_House', 'Income_Cats', 'Married_Flag']

X = df[features]
y = df.target

#One Hot Encoding
X = pd.get_dummies(X)

#Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.4,random_state=2)

#Initialize the Random Forest Model
rfm = RandomForestClassifier(random_state=2)
model = rfm.fit(X_train,y_train)
pred = model.predict(X_test)
rfm_acc_score = accuracy_score(pred,y_test)

print('Accuracy of base RFM is: '+str(rfm_acc_score))
print('Classification Report of RFM:')
print(classification_report(y_test, pred))

#Initialize and run KMeans Model
kmeans = KMeans(n_clusters=2,random_state=2,n_init=100)
model = kmeans.fit(X_train,y_train)
pred = model.predict(X_test)
kmeans_acc_score = accuracy_score(pred,y_test)

print('Accuracy is of Kmeans Clustering Model is: '+str(kmeans_acc_score))
print('Classification Report of Kmeans:')
print(classification_report(y_test, pred))
