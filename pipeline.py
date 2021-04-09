import os 
import torch
import video_bounding_box
import google_sheets
import pandas as pd
import numpy as np
import tqdm.auto as tqdm
import zipfile
import cv2

INPUT_FILE = 'kid_mixed.mp4'
FRAME_PATH = 'KID'

CLASS_NAMES = ['Angry', 'Disgusted', 'Fear', 'Happy', 'Sad', 'Surprised', 'Neutral']
#print("Unzipping models")
modellist = ['gender_detection.zip','emotion_detection_bounding_boxes.zip','emotion_detection.zip']

for modelname in modellist:
	with zipfile.ZipFile(modelname, 'r') as zip_ref:
		zip_ref.extractall('model')
		zip_ref.close()

def model_script(filepath):
	feat_score_fold_0,gender_array,time_array = video_bounding_box.show_boxes(filepath)
	#print(feat_score_fold_0)
	# feat_score_fold_1 = list()
	print("Ensembling models")
	feat_score_fold_0 = np.array(feat_score_fold_0)
	aggregated_score = np.add(feat_score_fold_0,feat_score_fold_0)/2
	row_sum = np.sum(aggregated_score,axis=1)
	aggregated_score = (aggregated_score/row_sum[:,np.newaxis])
	print("Creating aggregated_data")
	df = pd.DataFrame(aggregated_score, columns = CLASS_NAMES)
	df['Timestamp'] = time_array
	df['Gender'] = gender_array
	df = df[df['Gender'] != -1]
	df.replace(np.nan,0.0,inplace=True)
	from datetime import date
	today_date = str(date.today())
	df['Date'] = [today_date]*df.shape[0]
	count_file = open('counts.txt','r')
	count_val = int(count_file.read())
	count_file.close()

	#1st 2nd 3rd 4th 5th 6th 7th 8th 9th 0th
	
	df['Meeting_ID'] = [count_val]*df.shape[0]
	count_file = open('counts.txt','w')
	count_val += 1
	count_file.write(str(count_val))
	count_file.close()
	df = df[['Timestamp','Date','Meeting_ID','Gender','Happy','Sad','Angry','Disgusted','Fear','Surprised','Neutral']]
	print(df)
	df.to_csv('output.csv',index=False)
	arr = df.values.tolist()
	google_sheets.push_to_sheets(arr,"Emotion_Data")