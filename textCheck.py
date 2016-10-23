import json
import numpy
import random
import sys
	
from watson_developer_cloud import AlchemyLanguageV1

def tweetCheck (str, sensitivity,alchemy_language, arrayFile1, arrayFile2, arrayFile3, arrayFile4):
	sample = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	emotion = alchemy_language.emotion(text=str)
	sample[0] = float(emotion['docEmotions']['joy'])
	sample[1] = float(emotion['docEmotions']['disgust'])
	sample[2] = float(emotion['docEmotions']['fear'])
	sample[3] = float(emotion['docEmotions']['anger'])
	sample[4] = float(emotion['docEmotions']['sadness'])

	sentiment = alchemy_language.sentiment(text=str)
	sample[5] = 0
	if sentiment['docSentiment']['type'] != "neutral":
		sample[5] = float(sentiment['docSentiment']['score'])
	
	if sentiment['docSentiment']['type'] == "positive":
		diff1 = sample - arrayFile1['meanV']
		d1 = numpy.sqrt(numpy.dot(numpy.transpose(diff1),(numpy.dot(arrayFile1['covInv'], diff1))))
		print('WRT Fraud:')
		print(d1)
		
		p = ((float(sensitivity)-d1)/float(sensitivity))
		if p < 0:
			p = 0
		print(p)
		
		diff2 = sample - arrayFile2['meanV']
		d2 = numpy.sqrt(numpy.dot(numpy.transpose(diff2),(numpy.dot(arrayFile2['covInv'], diff2))))
		print('WRT Real: ')
		print(d2)

		p = ((float(sensitivity)-d2)/float(sensitivity))
		if p < 0:
			p = 0
		print(p)
	else:
		diff1 = sample - arrayFile3['meanV']
		d1 = numpy.sqrt(numpy.dot(numpy.transpose(diff1),(numpy.dot(arrayFile3['covInv'], diff1))))
		print('WRT Fraud:')
		print(d1)
		
		p = ((float(sensitivity)-d1)/float(sensitivity))
		if p < 0:
			p = 0
		print(p)
		
		diff2 = sample - arrayFile4['meanV']
		d2 = numpy.sqrt(numpy.dot(numpy.transpose(diff2),(numpy.dot(arrayFile4['covInv'], diff2))))
		print('WRT Real: ')
		print(d2)

		p = ((float(sensitivity)-d2)/float(sensitivity))
		if p < 0:
			p = 0
		print(p)
        if d1 > d2:
                s = "Likely real review. Statistically " + repr(d1/d2) + " times farther from the profile of fraud than the profile of real reviews. "  
        else:
                s = "Possible fraudulent review. Statistically " + repr(d2/d1) + " times farther from the profile of real reviews than from the profile of fraudulent reviews. "
        return s
def init(str):
	sensitivity = 3
        from watson_developer_cloud import AlchemyLanguageV1

	#Set up bluemix for emotion. 
	apikey = '922c007ff231ee81ac05c2b70c45ade7b0a717e5'

	arrayFile1 = numpy.load('PositiveFraudProfile.npz')
	arrayFile2 = numpy.load('PositiveRealProfile.npz')
	arrayFile3 = numpy.load('NegativeFraudProfile.npz')
	arrayFile4 = numpy.load('NegativeRealProfile.npz')
	alchemy_language = AlchemyLanguageV1(api_key=apikey)
	return tweetCheck(str, sensitivity, alchemy_language, arrayFile1, arrayFile2, arrayFile3, arrayFile4)
	
