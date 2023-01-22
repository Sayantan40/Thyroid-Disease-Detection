
from Thyroid.exception import ThyroidException
from Thyroid.logger import logging
from Thyroid.entity.config_entity import DataTransformationConfig 
from Thyroid.entity.artifact_entity import DataIngestionArtifact,\
DataValidationArtifact,DataTransformationArtifact
import sys,os
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
import pandas as pd
from Thyroid.constants import *
from Thyroid.utils.util import read_yaml_file,save_object,save_numpy_array_data,load_data
from sklearn.base import BaseEstimator,TransformerMixin
from imblearn.over_sampling import RandomOverSampler


class CustomTransformer(BaseEstimator,TransformerMixin):

    def fit(self, X, y=None):
        return self
    
    
    
    def fit_transform(self,X,y=None):
        
            try:
                lblEn = LabelEncoder()
                imputer=KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan)
                data = X.copy()
                data['sex'] = data['sex'].map({'F' : 0, 'M' : 1})
                cat_col = [col for col in data.columns if data[col].dtype==object]
                cat_col.remove('referral_source')
                for col in cat_col:
                    data[col] = lblEn.fit_transform(data[col])
                data = pd.get_dummies(data, columns=['referral_source'])
                data_array = imputer.fit_transform(data) 
                new_data = pd.DataFrame(data=np.round(data_array), columns=data.columns)
                return new_data
            except Exception as e:
                raise ThyroidException(e, sys) from e
        
    
    def transform(self,X,y=None):
        return self.fit_transform(X=X)

    
    
    def Randomizer(self,X,y=None):
        lblEn1 = LabelEncoder()
        rdsmple = RandomOverSampler()
        x1 = X
        y1 = y
        y1 = lblEn1.fit_transform(y1)
        x_sampled,y_sampled  = rdsmple.fit_resample(x1,y1)
        return np.array(x_sampled),y_sampled




class DataTransformation:

    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact
                 ):
        
        try:
            
            logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            
            self.data_transformation_config = data_transformation_config
            
            self.data_ingestion_artifact = data_ingestion_artifact
            
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise ThyroidException(e,sys) from e






    def initiate_data_transformation(self)-> DataTransformationArtifact :
        
        try:
            
            logging.info(f"Obtaining preprocessing object.")
            
            preprocessing_obj = CustomTransformer()
            
            logging.info(f"Obtaining training and test file path.")
            
            train_file_path = self.data_ingestion_artifact.train_file_path
            
            test_file_path = self.data_ingestion_artifact.test_file_path
            

            
            schema_file_path = self.data_validation_artifact.schema_file_path
            
            
            
            logging.info(f"Loading training and test data as pandas dataframe.")
            
            train_df = load_data(file_path = train_file_path, schema_file_path=schema_file_path)
            
            
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)

            
            schema = read_yaml_file(file_path=schema_file_path)
         
            unwanted_column_name = schema[UNWANTED_COLUMN_KEY] 

            target_column_name = schema[TARGET_COLUMN_KEY]

            logging.info(f"Splitting input and target feature from training and testing dataframe.")
            
            
            train_df = train_df.drop(columns=unwanted_column_name,axis=1)

            input_feature_train_df = train_df.drop(columns=target_column_name,axis=1)

            target_feature_train_df = train_df[target_column_name]



            test_df = test_df.drop(columns=unwanted_column_name,axis=1)

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)

            target_feature_test_df = test_df[target_column_name]

            
            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            
            input_feature_train_df = preprocessing_obj.fit_transform(X=input_feature_train_df)

            Randomizer = preprocessing_obj.Randomizer(X=input_feature_train_df, y=target_feature_train_df)

            input_feature_test_df = preprocessing_obj.transform(X=input_feature_test_df)

            Randomizer1 = preprocessing_obj.Randomizer(X=input_feature_test_df, y=target_feature_test_df)
            
            
            input_feature_train_df = Randomizer[0]
            
            target_feature_train_df = Randomizer[1]

            input_feature_test_df = Randomizer1[0]

            target_feature_test_df = Randomizer1[1]
            

            train_arr = np.c_[(input_feature_train_df,target_feature_train_df)]

            test_arr = np.c_[(input_feature_test_df,target_feature_test_df)]
            
            
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            
            
            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")

            
            
            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            
            logging.info(f"Saving transformed training and testing array.")
            
            
            save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)
            
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)

            
            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path

            
            logging.info(f"Saving preprocessing object.")
            
            save_object(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)

            
            
            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
                                                                      
                                                                      message="Data transformation successfull.",
                                                                      
                                                                      transformed_train_file_path=transformed_train_file_path,
                                                                      
                                                                      transformed_test_file_path=transformed_test_file_path,
                                                                      
                                                                      preprocessed_object_file_path=preprocessing_obj_file_path
                                                                      )
            
            
            logging.info(f"Data transformationa artifact: {data_transformation_artifact}")
            
            return data_transformation_artifact
        
        
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")  