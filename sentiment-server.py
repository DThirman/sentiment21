import os
import math
import pickle
import string
import json
from flask import Flask, request
#from apiclient.discovery import build

#import from the 21 Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment
def train(dir):
	wordDict = {}
	count = 0
	for rev in os.listdir(dir):
		count += 1
		with(open(dir+rev, 'r')) as f:
			review =  filter(lambda x: (x>='a' and x<='z') or (x>='A' and x<='Z') or x == ' ', f.read())
			words = set(review.split(' '))
			reviewWords = []
			for word in words:
				if len(word)>0:
					if word not in wordDict:
						wordDict[word] = 0.0
					wordDict[word] += 1.0

	wordDict = dict(map(lambda k,v: (k, math.log(v/count)), wordDict.iteritems()))

	return wordDict

def generateDict():
	pos =  train('txt_sentoken/pos/')
	neg =  train('txt_sentoken/neg/')
	pickle.dump((pos, neg), open('dict.pickle', 'wb'))

def sentiment(text):
	dicts = pickle.load(open('dict.pickle', 'rb'))
	posScore = 0
	negScore = 0
	words = set(text.lower().split(' '))
	transtable = {ord(c): None for c in string.punctuation}
	for word in words:
		word = word.translate(transtable)
		if word in dicts[0] and word in dicts[1]:
			posScore += dicts[0][word]
			negScore += dicts[1][word]
	return posScore/(posScore+negScore)

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)


@app.route('/sentiment')
@payment.required(200)
def trans():
    #print(request.get_data)
    text = request.args.get('text')
    sent = sentiment(text)
    print(sent)
    return str(sent)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #print(sentiment("hi, i am terrible"))