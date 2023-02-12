import mysql.connector
from mysql.connector import Error
import pandas as pd
import pickle
from feature_engine.outliers import Winsorizer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pickle
import numpy as np
class makepiple:
      datatest=''
      def __init__(self):
          try:
            connection = mysql.connector.connect(host='localhost',
                                                database='db_panel',
                                                user='root',
                                                password='9493',
                                                auth_plugin='mysql_native_password')
            if connection.is_connected():
                        db_Info = connection.get_server_info()
                        print("Connected to MySQL Server version ", db_Info)
                        cursor = connection.cursor()
                        cursor.execute("select * from user_test;")
                        real_test = pd.DataFrame(cursor.fetchall())
                        real_test.columns = list(cursor.column_names)
          except Error as e:
           print("Error while connecting to MySQL", e)
          real_test.rename(columns = {'Iff':'If'}, inplace = True)
          makepiple.datatest=real_test
class deploymentsetup(makepiple):
      model_passdata={}
      def __intit__(self):
          super.__init__(self)
      def piplinestepuptest(self,testdata):
          self.model_passdata=testdata
          print('before',self.model_passdata)
          for i,j in self.model_passdata.items():
              self.scale_min_max(i,j)
          return self.model_passdata        
      def scale_min_max(self,key,value):
                data_csv=pd.read_csv(r'E:\project-92\pycode\modelcode\modelslist\eda_win_scale.csv')
                data_csv.set_index('index',inplace=True)
                min_,max_,median=data_csv.at['min',key],data_csv.at['max',key],data_csv.at['50%',key]
                if(float(self.model_passdata[key])<=float(min_)):
                    self.model_passdata[key]=float(min_)
                elif(float(self.model_passdata[key])>=float(max_)):
                    self.model_passdata[key]=float(max_)
                z=(float(self.model_passdata[key]) - data_csv.at['mean',key]) / data_csv.at['std',key]
                self.model_passdata[key]=z




                '''pipe=Pipeline(steps=[('win',Winsorizer(tail='both',fold=1.5,capping_method='iqr',variables=['Ipv', 'Vpv', 'Vdc', 'ia', 'ib', 'ic', 'va', 'vb', 'vc', 'Iabc','If', 'Vabc', 'Vf'])),('std',StandardScaler())],verbose = True)
                pipe.fit_transform(self.testdata)'''
                #return self.testdata.columns
      def results(self,arr):
          res=''
          randomforestmodel=open(r"E:\project-92\pycode\modelcode\modelslist\randomforst.pkl",mode='rb')
          randomforestmodel=pickle.load(randomforestmodel)
          print(type(arr))
          if(type(arr)==dict):
            arr=pd.DataFrame.from_dict(arr,orient='index').transpose()
            value=randomforestmodel.predict(arr)
            arr['target']=value
            arr.reset_index(drop=True,inplace=True)
            if(arr.at[0,'target']=='F0L'):
                res="The Observation is Fault-free"
            else:
                res="The Observation is Fault"
          else:
            value=randomforestmodel.predict(arr)
            arr['target']=value


          return arr,res
      def filepre_processing(self,uploadedfile):
          test=pd.read_csv(uploadedfile)
          test.fillna(value=test.mean(), inplace=True)
          pipe=Pipeline(steps=[('removenan',test.fillna(value=test.mean(), inplace=True)),('win',Winsorizer(tail='both',fold=1.5,capping_method='iqr',variables=['Ipv', 'Vpv', 'Vdc', 'ia', 'ib', 'ic', 'va', 'vb', 'vc', 'Iabc','If', 'Vabc', 'Vf'])),('std',StandardScaler())],verbose = True)
          pipe.fit_transform(test)
          return self.results(test)
          
          
          

          
          

          







            

                



