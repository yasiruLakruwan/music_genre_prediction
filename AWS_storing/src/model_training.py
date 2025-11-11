import numpy as np
import pandas as pd
import os
import librosa
from logger import get_logger
from custom_exeption import CustomExeption
import matplotlib.pyplot as plt
from config.data_paths import *
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D,MaxPooling2D,Flatten,Dense,Dropout,BatchNormalization

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self,train_path,test_path):
        self.train_path = train_path
        self.test_path = test_path

    def data_processing(self):
        logger.info("Starting train data and test data collecting....")

        try:
            train_ds = image_dataset_from_directory(
                self.train_path,
                image_size = (128,128),
                batch_size = BATCH_SIZE,
                label_mode = 'categorical' # Multiclass
            )

            test_ds = image_dataset_from_directory(
                self.test_path,
                image_size = (128,128),
                batch_size = BATCH_SIZE,
                label_mode = 'categorical'
            )
            logger.info("Complete the train data and test data collecting....")
            return train_ds,test_ds
        except Exception as e:
            logger.error("Error while data accessing...")
            raise CustomExeption("Error while data accessing...",e)
            
    def model_building(self):
        try:
            train_ds,test_ds = self.data_processing()
            num_classes = len(train_ds.class_names)

            model = Sequential([
                Conv2D(32,(3,3),activation='relu',input_shape=(128,128,3)),
                MaxPooling2D(2,2),
                BatchNormalization(),

                Conv2D(64,(3,3),activation='relu'),
                MaxPooling2D(2,2),
                BatchNormalization(),

                Conv2D(128,(3,3),activation='relu'),
                MaxPooling2D(2,2),
                BatchNormalization(),

                Flatten(),
                Dense(128,activation='relu'),
                Dropout(0.2),
                Dense(num_classes,activation='softmax')
            ])

            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            logger.info("Model build and compiled successfully...")
            return model
        
        except Exception as e:
            logger.error("Error while model building.....")
            raise CustomExeption("Error while model building...",e)
        
    def model_training(self):
        try:
            model = self.model_building()
            train_ds,test_ds = self.data_processing()
            history = model.fit(
                train_ds,
                validation_data = test_ds,
                epochs = 5
            )
            logger.info("Model trained successfully....")
            os.makedirs(os.path.dirname(MODEL_SAVE_PATH),exist_ok=True)
            model.save(MODEL_SAVE_PATH)
            logger.info(f"Model save to {MODEL_SAVE_PATH} successfully....")

        except Exception as e:
            logger.error("Error while model training...")
            raise CustomExeption("Error hapening in model training",e)
        
    def run(self):
        self.data_processing()
        self.model_building()
        self.model_training()   

if __name__=="__main__":
    training = ModelTraining(TRAIN_DIR,TEST_DATA)
    training.run()