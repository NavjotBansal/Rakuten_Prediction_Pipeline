import os 
import torch
import video_bounding_box
import pandas as pd
import numpy as np
import tqdm.auto as tqdm
import zipfile
import cv2
import time 
from datetime import date
import datetime
import math
from csv import writer

INPUT_FILE = 'kid_small.mp4'
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
	feat_score_fold_0 = np.array(feat_score_fold_0,dtype=float)
	aggregated_score = np.add(feat_score_fold_0,feat_score_fold_0)/2
	row_sum = np.sum(aggregated_score,axis=1)
	aggregated_score = (aggregated_score/row_sum[:,np.newaxis])
	aggregated_score=np.round(aggregated_score, 4)

	print("Creating aggregated_data")
	df = pd.DataFrame(aggregated_score, columns = CLASS_NAMES)
	timenow = time.time()
	time_string = list()
	for i in range(len(time_array)):
		now = datetime.datetime.now()
		time_array[i] += timenow
		timedata = datetime.datetime.fromtimestamp(time_array[i]).strftime('%I:%M:%S %p')
		time_string.append(f'{timedata}')
	df['Timestamp'] = time_string
	df['Gender'] = gender_array
	df = df[df['Gender'] != -1]
	df.replace(np.nan,0.0,inplace=True)
	today_date = str(date.today().strftime("%d-%b-%y"))
	df['Date'] = [today_date]*df.shape[0]
	count_file = open('counts.txt','r')
	count_val = int(count_file.read())
	count_file.close()

	#1st 2nd 3rd 4th 5th 6th 7th 8th 9th 0th
	
	df['Meeting_ID'] = [count_val]*df.shape[0]
	count_file = open('counts.txt','w')
	count_file.write(str(count_val + 1))
	count_file.close()
	df = df[['Timestamp','Date','Meeting_ID','Gender','Happy','Sad','Angry','Disgusted','Fear','Surprised','Neutral']]
	print(df)
	arr = df.values.tolist()
	df.to_csv('Emotion_Data.csv', header= False, index = False,mode='a',line_terminator="\n")

	max_participants = max(4,time_array.count(max(time_array)))

	meeting_data_df = pd.DataFrame()
	meeting_data_df['Meeting ID1']=[count_val]*1
	meeting_data_df['Start Time']=[datetime.datetime.fromtimestamp(time_array[0]).strftime('%I:%M:%S %p')]*1
	meeting_data_df['End Time']=[datetime.datetime.fromtimestamp(time_array[0]+1799).strftime('%I:%M:%S %p')]*1
	meeting_data_df['Date (Meeting Data.csv)']= [today_date]*1
	meeting_data_df['Distinct No. of Participants'] = [max_participants]*1
	meeting_data_df['Class Size']=[10]*1
	print(meeting_data_df)
	meeting_data_df.to_csv('Meeting_Data.csv', header= False, index = False,mode='a',line_terminator="\n")
	#use this for second sheet
	meeting_data_arr = meeting_data_df.values.tolist()
	print(meeting_data_arr)
	participant_data_df = pd.DataFrame()
	participant_data_df['Meeting ID1']=[count_val]*max_participants
	participantid = list()
	participantjoin = list()
	Participantleft =list()
	for i in range(1,max_participants+1):
		participantid.append(i)
		participantjoin.append(str(datetime.datetime.fromtimestamp(time_array[0]+i*20).strftime('%I:%M:%S %p')))
		Participantleft.append(str(datetime.datetime.fromtimestamp(time_array[0]+1799-i*30).strftime('%I:%M:%S %p')))
	participant_data_df['Participant ID']=participantid
	participant_data_df['Join Time']=participantjoin
	participant_data_df['Leave Time']=Participantleft
	print(participant_data_df)
	participant_data_df.to_csv('Participant_Data.csv', header= False, index = False,mode='a',line_terminator="\n")
	#use this for thrid sheet
	participant_data_arr = participant_data_df.values.tolist()