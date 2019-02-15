from app.Healthcare_EDA_functions import *
import numpy as np
import pandas as pd
import re

from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import GradientBoostingClassifier

#Modify the supervisor variable and add the Supervisor Rating
class Rate_Supervisor(TransformerMixin):

    def __init__(self,d_supervisors):
        self.goodL1 = d_supervisors['goodL1']
        self.badL1 = d_supervisors['badL1']
        self.goodL2 = d_supervisors['goodL2']
        self.badL2 = d_supervisors['badL2']
        pass

    def transform(self,X,y=None):
        #Fix L1 Supervisor Ratings
        badL1_lst=self.badL1
        goodL1_lst = self.goodL1
        X['L1_Supervisor_Rating'] = X.L1Supervisor.apply(lambda x: sortL1(x,badL1_lst,goodL1_lst))
        #Fix L2 Supervisor Ratings
        badL2_lst=self.badL2
        goodL2_lst = self.goodL2
        X['L2_Supervisor_Rating'] = X.L2Supervisor.apply(lambda x: sortL2(x,badL2_lst,goodL2_lst))
        return X

    def fit(self,X,y):
        return self

#Split the Designation variable into three component pieces
class Split_Designation(TransformerMixin):

    def __init__(self):
        pass

    def transform(self,X,y=None):
        X = pd.DataFrame(X)
        X['primary_designation'] = X.Designation.apply(split_desig_prim)
        X['secondary_designation'] = X.Designation.apply(split_desig_sec)
        X['descriptor_designation'] = X.Designation.apply(split_desig_des)
        X['secondary_designation'] = X.secondary_designation.fillna('not_assigned')
        return X

    def fit(self,X,y):
        return self

#Add the Client Rating variable
class Rate_Clients(TransformerMixin):

    def __init__(self):
        pass

    def transform(self,X,y=None):
        clients_bad = ['ALN', 'Athena', 'Brightree', 'Cymetrix', 'HAP', 'PPM', 'Source Medical', 'TPX']
        clients_good = ['Altruis', 'Continuum', 'MRG', 'Shared Services', 'T-Systems', 'Zotec', 'abeo']
        bad_clients = clients_bad
        good_clients = clients_good
        X['Client_Rating'] = X.Client.apply(lambda x: sortClients(x,bad_clients,good_clients))
        return X

    def fit(self,X,y):
        return self

#Split the Functionality Variable
class Split_Functionality(TransformerMixin):

    def __init__(self):
        pass

    def transform(self,X,y=None):
        X['secondary_functionality'] = X.Functionality.apply(split_functionality)
        X['primary_functionality']=X.Functionality.apply(split_functionality2)
        X['secondary_functionality']=X.secondary_functionality.fillna('none')
        return X

    def fit(self,X,y):
        return self


#Create the variables relating to age_at_join
class Calc_Age(TransformerMixin):

    def __init__(self):
        pass

    def transform(self,X,y=None):
        X['age_at_join'] = (X['DOJ'] - X['DOB']) #/ np.timedelta64(1, 'D')
        return X

    def fit(self,X,y):
        return self



#Modify the Pincode Variable and add Districts and Moved variable
class Add_District(TransformerMixin):

    def __init__(self):
        pass

    def import_districts(district_file):
        pin_tab = pd.read_csv(district_file,encoding='ISO-8859-1')
        pin_tab = pin_tab.loc[0::,['pincode','Districtname','statename']]
        pin_tab=pin_tab.drop_duplicates(subset='pincode',keep='first')
        return pin_tab

    def add_districts(X,pin_tab):
        X = pd.merge(left=X,right=pin_tab[['Districtname']],left_on=['Pre_Pincode'],right_on=pin_tab['pincode'],how='left')
        X['Districts'] = X.Districtname.apply(district_group)
        X.Districts.fillna('Unknown',inplace=True)
        return X

    def add_moved(X):
        X['Per_Pincode'] = np.where(X['Per_Pincode'].isnull(),X['Pre_Pincode'],X['Per_Pincode'])
        X['Moved'] = np.where(X['Pre_Pincode']==X['Per_Pincode'],'no','yes')
        return X

    def transform(self,X,y=None):
        pin_tab = Add_District.import_districts('app/static/all_india_pin_code.csv')
        X = Add_District.add_districts(X,pin_tab)
        X = Add_District.add_moved(X)
        return X

    def fit(self,X,y):
        return self


#Cleanup the Highest Degree field
class Clean_HighestDegree(TransformerMixin):

    def __init__(self):
        pass

    def transform(self,X,y=None):
        X.HighestDegree.fillna('None',inplace=True)
        X['HighestDegree'] = X.HighestDegree.astype(str)
        X['HighestDegree'] = X.HighestDegree.apply(clean_column)
        X['HighestDegree'] = X.HighestDegree.apply(RepBSC)
        X['HighestDegree'] = X.HighestDegree.apply(RepBCOM)
        X['HighestDegree'] = X.HighestDegree.apply(RepBE)
        X['HighestDegree'] = X.HighestDegree.apply(RepBCA)
        X['HighestDegree'] = X.HighestDegree.apply(RepBPHARM)
        X['HighestDegree'] = X.HighestDegree.apply(RepBTECH)
        X['HighestDegree'] = X.HighestDegree.apply(RepBA)
        X['HighestDegree'] = X.HighestDegree.apply(RepMSC)
        X['HighestDegree'] = X.HighestDegree.apply(RepMBA)
        X['HighestDegree'] = X.HighestDegree.apply(RepBCS)
        X['HighestDegree'] = X.HighestDegree.apply(RepBBA)
        X['HighestDegree'] = X.HighestDegree.apply(RepBBM)
        X['HighestDegree'] = X.HighestDegree.apply(RepMCA)
        X['HighestDegree'] = X.HighestDegree.apply(RepBE2)
        X['HighestDegree'] = X.HighestDegree.apply(RepDip)
        X['HighestDegree'] = X.HighestDegree.apply(MPharm)
        X['HighestDegree'] = X.HighestDegree.apply(clean_desig)
        X['degree_title'] = X.HighestDegree.apply(split_degree)
        return X

    def fit(self,X,y):
        return self

#Create the total leaves variable
class Add_Leaves(TransformerMixin):

    def __init__(self):
        self.sick = X.NoOfSickLeaveAvailed
        self.casual = X.NoOfCLAvailed
        pass

    def transform(self,X,y=None):
        X['total_leaves'] = self.casual + self.sick
        return X

    def fit(self,X,y):
        return self

#Add misc. variables
class Add_Vars(TransformerMixin):

    def __init__(self):
        pass

    def transform(self,X,y=None):
        X['Operation_Assistant'] = np.where(((X['primary_functionality']=='operations') &
                                       (X['primary_designation']=='assistant')),1,0)
        X['Shared_Software'] = np.where(((X['primary_functionality']=='shared services') &
                                       (X['primary_designation']=='software')),1,0)
        X=X.rename(columns={'Productivity%':'Productivity','Quality%':'Quality'})
        #Variable for when Productivity is null and Quality isn't
        X['NullProd'] = np.where((X.Productivity.isnull() & X.Quality.notnull()),1,0)
        #Variable for when Quality is null and Productivity isn't
        X['NullQual'] = np.where((X.Quality.isnull() & X.Productivity.notnull()),1,0)
        #Variable for when both Productivity and Quality are null
        X['Both_Null_Prod_Qual'] = np.where((X.Quality.isnull() & X.Productivity.isnull()),1,0)
        return X

    def fit(self,X,y):
        return self


#Keep only useful features
class Keep_Features(TransformerMixin):

    def __init__(self):
        self.feats =['Gender','primary_designation','secondary_designation',\
           'Client','secondary_functionality','MaritalStatus','NullProd','NullQual','Both_Null_Prod_Qual',\
           'HighestDegree','primary_functionality','Districts','PrevCompanyExp','Moved',\
           'total_leaves','age_at_join','degree_title','Dependents','Productivity','LateEntry',\
           'Operation_Assistant','Shared_Software','Shift']
        pass

    def transform(self,X,y=None):

        X = X[self.feats]
        return X

    def fit(self,X,y):
        return self

#Create dummy variables
class Dummy(TransformerMixin):

    def __init__(self,d_accepted):
        self.d_accepted = d_accepted
        pass

    def transform(self,X,y=None):
        for var in X.columns:
            if X[var].dtypes == object:
                X[var] = pd.Categorical(X[var],self.d_accepted[var])
        X = pd.get_dummies(X)
        return X

    def fit(self,X,y):
        return self


#Impute values for Productivity
class Impute(TransformerMixin):

    def __init__(self,mean):
        self.mean = mean
        pass

    def transform(self,X,y=None):
        X['Productivity']=X.Productivity.fillna(self.mean)
        return X

    def fit(self,X,y):
        return self
