import os 
import torch
import video_bounding_box
import pandas as pd
import numpy as np
import tqdm.auto as tqdm
import zipfile
import cv2

INPUT_FILE = 'input-zoom.mp4'
FRAME_PATH = 'KID'

CLASS_NAMES = ['Angry', 'Disgusted', 'Fear', 'Happy', 'Sad', 'Surprised', 'Neutral']
#print("Unzipping models")
modellist = ['gender_detection.zip','emotion_detection_bounding_boxes.zip','emotion_detection.zip']

for modelname in modellist:
	with zipfile.ZipFile(modelname, 'r') as zip_ref:
		zip_ref.extractall('model')
		zip_ref.close()

if __name__ == '__main__':
	feat_score_fold_0,gender_array,time_array = video_bounding_box.show_boxes(INPUT_FILE)
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
	df = df[df['Gender'] != 'None']
	df = df[['Timestamp','Gender','Happy','Sad','Angry','Disgusted','Fear','Surprised','Neutral']]
	print(df)
	df.to_csv('output.csv',index=False)
