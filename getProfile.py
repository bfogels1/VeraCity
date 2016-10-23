import json
import numpy
import sys
import os

from watson_developer_cloud import AlchemyLanguageV1
from numpy.linalg import inv

#Set up bluemix for emotion. 
apikey = '922c007ff231ee81ac05c2b70c45ade7b0a717e5'

numRevs = int(sys.argv[1])

width, height = numRevs, 6
m = [[0.0 for col in range(width)] for row in range(height)]

filePath = 'C:/Users/MLH-Admin/Desktop/HopHacks/'
dataSets = ['PositiveFraud', 'PositiveReal', 'NegativeFraud', 'NegativeReal']

for dataSet in dataSets:
	col = 0
	alchemy_language = AlchemyLanguageV1(api_key=apikey)
	for file in os.listdir(filePath + dataSet):
		print(file)
		inFile = open(filePath + dataSet + '/' + file, 'r')
		fileText = inFile.read()
		print(fileText)
		
		emotion = alchemy_language.emotion(text=(fileText))
		m[0][col] = float(emotion['docEmotions']['joy'])
		m[1][col] = float(emotion['docEmotions']['disgust'])
		m[2][col] = float(emotion['docEmotions']['fear'])
		m[3][col] = float(emotion['docEmotions']['anger'])
		m[4][col] = float(emotion['docEmotions']['sadness'])
		
		sentiment = alchemy_language.sentiment(text=(fileText))
		m[5][col] = 0
		if sentiment['docSentiment']['type'] != "neutral":
			m[5][col] = float(sentiment['docSentiment']['score'])
		col+=1
		inFile.close()
	matrix = numpy.matrix(m)
	
	for row in range(height):
		meanV = numpy.mean(m, axis=1, dtype=None, out=None, keepdims=False)
	
	covM = numpy.cov(matrix)

	covInv = inv(covM)

	numpy.savez(dataSet + 'Profile', meanV=meanV, covInv=covInv)
	arrayFile = numpy.load(dataSet + 'Profile.npz')

	print('Wrote emotion profile to' + dataSet + 'Profile.npz. ')
	print('Mean Vector: ')
	print(meanV)
	print('Covariance Vector (inverse is stored): ')
	print(covM)