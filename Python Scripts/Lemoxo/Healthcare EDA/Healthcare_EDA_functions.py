#This is a collection of the functinos defined and used as a part of the:
#Access Healthcare EDA
import re as re
#Designation
def split_desig_prim(x):
    x = x.lower().split(' ')
    x = x[0]
    x = re.sub("[^a-zA-Z]","",x)
    x = x.strip('\n')
    return x

def split_desig_sec(x):
    x = x.lower().split(' ')
    x = x[1::]
    y = ''
    for word in x:
        y = y + word + ' '
    y=y.strip('\n')
    return y

def split_desig_des(x):
    x = x.lower().split('-')
    if len(x)>1:
        y = x[-1].strip(" ")
        return y
    else:
        return 'None'

def split_desig2(x):
    x = x.lower().split('-')
    return x[0]

def split_dash(x):
    x_lst = x.split('-')
    if len(x_lst)==1:
        x_lst = x.split(' - ')
    if len(x_lst)==1:
        x_lst = x.split('–')
    if len(x_lst)==1:
        x_lst = x.split(' – ')
    return x_lst[0]

#Functionality
def split_functionality(x):
    y = x.lower().split('-')
    if len(y)>1:
        return y[-1].strip(' ')
    else:
        z = x.lower().split('–')
        if len(z)>1:
            return z[-1].strip(' ')

def split_functionality2(x):
    y = x.lower().split('-')
    #y = x[0].lower().split('–')
    if len(y)==1:
        y = x.lower().split('–')
    y = y[0].split(' – ')
    z = y[0].strip(' ')
    if z[-1] != 's':
        z = z+'s'
    return z


#HighestDegree
def clean_column(x):
    x = x.lower()
    x = re.sub("[^a-zA-Z ]","",x)
    return x

def RepBSC(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:3]
    if (degree == 'bsc') | (y == 'bachelorofscience'):
        return 'Bachelor of Science'
    else:
        return x

def RepBCOM(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:4]
    if (degree == 'bcom') | (y == 'bachelorofcommerce') | (y=='commerce'):
        return 'Bachelor of Commerce'
    else:
        return x

def RepBE(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:2]
    if (degree == 'be') | (y == 'bachelorofengineering') | (y=='engineering'):
        return 'Bachelor of Engineering'
    else:
        return x

def RepBCA(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:3]
    if (degree == 'bca') | (y == 'bachelorofcomputerapplicati') | (y=='computerapplication'):
        return 'Bachelor of Computer Application'
    else:
        return x

def RepBPHARM(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:6]
    if (degree == 'bpharm') | (y == 'bpharmacy') | (y=='pharmacy'):
        return 'Bachelor of Pharmacy'
    else:
        return x

def RepBTECH(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:5]
    if (degree == 'btech') | (y == 'bacheloroftechnology'):
        return 'Bachelor of Technology'
    else:
        return x

def RepBA(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:2]
    if (degree == 'ba') | (y == 'bachelorofarts'):
        return 'Bachelor of Arts'
    else:
        return x

def RepMSC(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:3]
    if (degree == 'msc') | (y == 'masterofscience'):
        return 'Master of Science'
    else:
        return x

def RepMBA(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:3]
    if (degree == 'mba') | (y == 'masterofbusinessadministration'):
        return 'Master of Business Administration'
    else:
        return x

def RepBCS(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:3]
    if (degree == 'bcs') | (y == 'bachelorofcomputer science') | (y=='computerscience'):
        return 'Bachelor of Computer Science'
    else:
        return x

def RepBBA(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:3]
    if (degree == 'bba') | (y == 'bachelorofbusinessadministration') | (y=='businessadministration'):
        return 'Bachelor of Business Administration'
    else:
        return x

def RepBBM(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:3]
    if (degree == 'bbm') | (y == 'bachelorofbusinessmanagement') | (y=='businessmanagement'):
        return 'Bachelor of Business Management'
    else:
        return x

def RepMCA(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:3]
    if (degree == 'mca') | (y == 'masterofcomputerapplication'):
        return 'Master of Computer Application'
    else:
        return x

def RepBE2(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:2]
    if ('engineering' in y) & ('master' not in y):
        return 'Bachelor of Engineering'
    else:
        return x

def RepDip(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:1]
    if ('diploma' in y) | (degree=='d'):
        return 'Diploma'
    else:
        return x

def MPharm(x):
    y = re.sub("[^a-zA-Z]","",x)
    degree = y[0:1]
    if (('pharma' in y) | ('mpharma' in y)) & ('Bachelor' not in y) & ('bachelor' not in y):
        return 'Master of Pharmacy'
    else:
        return x

def split_degree(x):
    x = x.lower().split(' ')
    if x[0] == 'bachelor':
        return 'Bachelor'
    elif x[0] == 'master':
        return 'Masters'
    elif x[0] == 'diploma':
        return 'Diploma'
    elif x[0]=='nan':
        return 'NoData'
    else:
        return 'Others'
    
def clean_desig(x):
    degrees = ['Bachelor of Science','Bachelor of Commerce','Bachelor of Computer Application','Bachelor of Engineering',\
              'Bachelor of Arts','none','Diploma','Master of Science','Bachelor of Technology','Bachelor of Business Administration',\
              'Bachelor of Pharmacy','Master of Business Administration','Master of Computer Application','Bachelor of Computer Science',\
              'Bachelor of Business Management','Master of Pharmacy']
    if x in degrees:
        return x
    else:
        return 'Other'

#Pincode
def district_group(x):
    districts = ['Chennai','Pune','Tiruvallur','Kanchipuram','Coimbatore']
    if x not in districts:
        return 'Other'
    else:
        return x

#Supervisor
def sortL1(x,badL1_lst,goodL1_lst):
    if x in badL1_lst:
        return 'Bad'
    elif x in goodL1_lst:
        return 'Good'
    else:
        return 'Neutral'

def sortL2(x,badL2_lst,goodL2_lst):
    if x in badL2_lst:
        return 'Bad'
    elif x in goodL2_lst:
        return 'Good'
    else:
        return 'Neutral'

def sortClients(x,bad_clients,good_clients):
    if x in bad_clients:
        return 'Bad'
    elif x in good_clients:
        return 'Good'
    else:
        return 'Neutral'
































        
