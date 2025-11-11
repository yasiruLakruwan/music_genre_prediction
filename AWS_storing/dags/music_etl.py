import random
import shutil
from airflow.decorators import dag,task
from datetime import datetime
import os
import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import boto3

#---ETL PIPELINE: Extract->Transform->Load---


@dag(
    schedule=None,
    start_date=datetime(2025,1,1),
    catchup=False,
    tags=["etl","music","astro"]
)

def music_etl():  
    #EXTRACT PART
    @task()
    def extract_audio_from_s3():
        print("Extracting audio from s3")
        ## Download all .au files from S3
        import csv

        aws_key_path = "/usr/local/airflow/include/yasiru_accessKeys.csv"
        with open(aws_key_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            # Normalize headers
            reader.fieldnames = [h.strip() for h in reader.fieldnames]
            print("CSV headers found:", reader.fieldnames)

            rows = list(reader)
            if not rows:
                raise ValueError(f"No credentials found in CSV: {aws_key_path}")

            creds = {k.strip(): v.strip() for k, v in rows[0].items()}
            print("Credential keys:", creds.keys())

        aws_access_key = creds['Access key ID']
        aws_secret_key = creds['Secret access key']

        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name="us-east-1"
        )
        bucket_name = "music-genre-dataset-yasiru"
        prefix = "genres/"
        local_dir = "/usr/local/airflow/include/audio/"
        os.makedirs(local_dir,exist_ok=True)

        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket= bucket_name,Prefix=prefix):
            for object in page.get("Contents",[]):
                key = object["Key"]
                if key.endswith(".au"):
                    # Keep genre folders locally
                    subfolder = key.split("/")[1]
                    genre_path = os.path.join(local_dir,subfolder)
                    os.makedirs(genre_path,exist_ok=True)

                    local_path = os.path.join(genre_path,os.path.basename(key))
                    s3.download_file(bucket_name,key,local_path)
                    print(f"Download {key} --> {local_path}")
        return local_dir
    
    #TRANSFORM
    @task
    def transform_to_melspectograms(local_dir: str):
        """Convert all .au audio files into mel-spectrogram images"""
        print("Starting transform to melspectograms")
        output_dir = "/usr/local/airflow/include/melspectrograms/"
        os.makedirs(output_dir,exist_ok=True)

        for genre in os.listdir(local_dir):
            genre_path = os.path.join(local_dir, genre)
            if os.path.isdir(genre_path):
                output_genre_dir = os.path.join(output_dir, genre)
                os.makedirs(output_genre_dir, exist_ok=True)

                for f in os.listdir(genre_path):
                    if f.endswith(".au"):  # <-- updated extension
                        file_path = os.path.join(genre_path, f)
                        y, sr = librosa.load(file_path, sr=None)
                        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
                        S_dB = librosa.power_to_db(S, ref=np.max)

                        # Plot and save mel-spectrogram
                        plt.figure(figsize=(3, 3))
                        librosa.display.specshow(S_dB, sr=sr)
                        plt.axis("off")

                        output_path = os.path.join(output_genre_dir, f.replace(".au", ".png"))
                        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
                        plt.close()

                        print(f"Generated mel-spectrogram: {output_path}")

        return output_dir
    #loading data in to train test folders
    @task
    def spliting_data(output_dir):
        print("Splitting the data")
        
        train_dir = "/usr/local/airflow/include/train_data/"
        test_dir = "/usr/local/airflow/include/test_data/"

        os.makedirs(train_dir,exist_ok=True)
        os.makedirs(test_dir,exist_ok=True)

        for genre in os.listdir(output_dir):
            genre_path = os.path.join(output_dir,genre)

            if not os.path.isdir(genre_path):
                continue
            files = [f for f in os.listdir(genre_path) if f.endswith(".png")]
            random.shuffle(files)   

            split_index = int(0.9 * len(files))
            train_files = files[:split_index]
            test_files = files[split_index:]

            # Create genre subfolders
            train_genre_dir = os.path.join(train_dir, genre)
            test_genre_dir = os.path.join(test_dir, genre)
            os.makedirs(train_genre_dir, exist_ok=True)
            os.makedirs(test_genre_dir, exist_ok=True)

            # Copy files
            for f in train_files:
                shutil.copy(os.path.join(genre_path, f), os.path.join(train_genre_dir, f))
            for f in test_files:
                shutil.copy(os.path.join(genre_path, f), os.path.join(test_genre_dir, f))

            print(f"Genre '{genre}': {len(train_files)} train, {len(test_files)} test")

        print(f"Data split complete: Train -> {train_dir}, Test -> {test_dir}")
        return {"train_dir": train_dir, "test_dir": test_dir}

      # --- TASK DEPENDENCIES ---
    audio_dir = extract_audio_from_s3()
    mel_dir = transform_to_melspectograms(audio_dir)
    spliting_data(mel_dir)

music_etl()