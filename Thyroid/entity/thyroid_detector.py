import os
import sys

from Thyroid.exception import ThyroidException
from Thyroid.utils.util import load_object

import pandas as pd


class ThyroidData:

    def __init__(self,
                
                age:float,
                 
                sex:str,
                 
                on_thyroxine:str,
                 
                query_on_thyroxine:str,
                 
                on_antithyroid_medication:str,
                 
                sick:str,
                 
                pregnant:str,
                 
                thyroid_surgery:str,
                 
                I131_treatment:str,

                query_hypothyroid:str,

                query_hyperthyroid: str,

                lithium : str,

                goitre:str,

                tumor:str,

                hypopituitary:str,

                psych:str,

                T3:float,

                TT4:float,

                T4U:float,

                FTI:float,

                referral_source_STMW:str,

                referral_source_SVHC:str,

                referral_source_SVHD:str,

                referral_source_SVI:str,

                referral_source_other:str,

                Class:str = None

                 
                 ):
        
        try:
            
            self.age = age
            
            self.sex = sex
            
            self.on_thyroxine = on_thyroxine
            
            self.query_on_thyroxine = query_on_thyroxine
            
            self.on_antithyroid_medication = on_antithyroid_medication
            
            self.sick = sick
            
            self.pregnant = pregnant
            
            self.thyroid_surgery = thyroid_surgery
            
            self.I131_treatment = I131_treatment
        
            self.query_hypothyroid =query_hypothyroid

            self.query_hyperthyroid = query_hyperthyroid
            
            self.lithium = lithium

            self.goitre = goitre

            self.tumor = tumor

            self.hypopituitary = hypopituitary

            self.psych = psych

            self.T3 = T3
      
            self.TT4 = TT4

            self.T4U = T4U

            self.FTI = FTI

            self.referral_source_STMW = referral_source_STMW

            self.referral_source_SVHC = referral_source_SVHC

            self.referral_source_SVHD = referral_source_SVHD

            self.referral_source_SVI = referral_source_SVI

            self.referral_source_other = referral_source_other
        
        
        except Exception as e:
            raise ThyroidException(e, sys) from e

    
    def get_Thyroid_input_data_frame(self):

        try:
            
            Thyroid_input_dict = self.get_Thyroid_data_as_dict()
            
            return pd.DataFrame(Thyroid_input_dict)
        
        except Exception as e:
            raise ThyroidException(e, sys) from e

    def get_Thyroid_data_as_dict(self):
        
        try:
            
            input_data = {
                "age": [self.age],
                
                "sex": [self.sex],
                
                "on_thyroxine": [self.on_thyroxine],
                
                "query_on_thyroxine": [self.query_on_thyroxine],
                
                "on_antithyroid_medication": [self.on_antithyroid_medication],
                
                "sick": [self.sick],
                
                "pregnant": [self.pregnant],
                
                "thyroid_surgery": [self.thyroid_surgery],

                "I131_treatment": [self.I131_treatment],

                "query_hypothyroid": [self.query_hypothyroid],

                "query_hyperthyroid": [self.query_hyperthyroid],

                "lithium": [self.lithium],

                "goitre": [self.goitre],

                "tumor": [self.tumor],

                "hypopituitary": [self.hypopituitary],

                "psych": [self.psych],

                "T3": [self.T3],

                "TT4": [self.TT4],

                "T4U": [self.T4U],

                "FTI": [self.FTI],

                "referral_source_STMW": [self.referral_source_STMW],

                "referral_source_SVHC": [self.referral_source_SVHC],

                "referral_source_SVHD": [self.referral_source_SVHD],

                "referral_source_SVI": [self.referral_source_SVI],

                "referral_source_other": [self.referral_source_other]
                
                
                }
            
            return input_data
        
        
        except Exception as e:
            raise ThyroidException(e, sys)


class ThyroidPredictor:

    def __init__(self, model_dir: str):
        
        try:
            
            self.model_dir = model_dir
        
        except Exception as e:
            raise ThyroidException(e, sys) from e

    
    def get_latest_model_path(self):
        
        try:
            
            folder_name = list(map(int, os.listdir(self.model_dir)))
            
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            
            file_name = os.listdir(latest_model_dir)[0]
            
            latest_model_path = os.path.join(latest_model_dir, file_name)
           
            return latest_model_path
        
        except Exception as e:
            raise ThyroidException(e, sys) from e

    def predict(self, X):
        
        try:
            
            model_path = self.get_latest_model_path()
            
            model = load_object(file_path=model_path)
            
            Class = model.predict_app(X)
            
            return Class
        
        except Exception as e:
            raise ThyroidException(e, sys) from e