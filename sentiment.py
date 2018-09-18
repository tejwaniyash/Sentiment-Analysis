import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights
twitter_consumer_key = 'YqM092IZN7fpjwzsTFhBOrUim'
twitter_consumer_secret = 'bsFZh765H4CDXLOMkuQDFBKShdVNjW9v8AQd3VNRdp7KTZqmUF'
twitter_access_token = '550134049-UjSYiTMsY8lsyv51wtV36zXzYqy2FSkqYEQnF1CF'
twitter_access_secret = 'Gakvv3NnkU1TfH4OwZhfaDHJsVhzD6eVPDvCfYy3M9qUi'

twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)
user_handle = "@dummy"




def analyze(handle):

	text="""
	I am not the only traveler
Who has not repaid his debt
I've been searching for a trail to follow again
Take me back to the night we met
And then I can tell myself
What the hell I'm supposed to do
And then I can tell myself
Not to ride along with you
I had all and then most of you
Some and now none of you
Take me back to the night we met
I don't know what I'm supposed to do
Haunted by the ghost of you
Oh, take me back to the night we met
When the night was full of terrors
And your eyes were filled with tears
When you had not touched me yet
Oh, take me back to the night we met
I had all and then most of you
Some and now none of you
Take me back to the night we met
I don't know what I'm supposed to do
Haunted by the ghost of you
Take me back to the night we met
"""

	pi_result = personality_insights.profile(text)
	return pi_result

def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data
def compare(dict1, dict2):
    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
                compared_data[keys]=abs(dict1[keys] - dict2[keys])
    return compared_data

pi_username = 'bc38c567-a7de-411e-a229-d31a1b74adc0'
pi_password = 'qcUHFnabG6qr'


personality_insights = PersonalityInsights(username=pi_username, password=pi_password)
user_result = analyze(user_handle)
user = flatten(user_result)
print ("User:")
for r in user:
  print (r, user[r]*100)

#print "The Relative result with your celebrity is : "
#for keys, value in sorted_result[:5]:
    #print keys,
    #print(user[keys]),
    #print ('->'),
    #print (celebrity[keys]),
    #print ('->'),
    #print (compared_results[keys])