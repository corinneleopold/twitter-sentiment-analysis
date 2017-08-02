from watson_developer_cloud import ToneAnalyzerV3
import json
import os
import sys

def get_credentials():
	# Load IBM Watson Tone Analyzer credentials from VCAP services environment variable
	if 'VCAP_SERVICES' in os.environ:
	    vcap = json.loads(os.getenv('VCAP_SERVICES'))
	    if 'tone_analyzer' in vcap:
	        creds = vcap['tone_analyzer'][0]['credentials']
	        user = creds['username']
	        pw = creds['password']
	else:
	    with open('vcap-local.json') as f:	# Read credentials from local vcap file
	        vcap = json.loads(f.read())
	        if 'tone_analyzer' in vcap:
	            creds = vcap['tone_analyzer']['credentials']
	            user = creds['username']
	            pw = creds['password']
	        else:
	            print("ERROR: Tone analyzer credentials not found")
	            sys.exit(0)

	tone_analyzer = ToneAnalyzerV3(
	  version='2017-05-25',
	  username=user,
	  password=pw
	)
	return tone_analyzer

# Calls Watson tone analyzer to retrieve sentiments for text
# Returns json output from tone analyzer
def get_sentiment(text):
	tone_analyzer = get_credentials()
	tone = tone_analyzer.tone(text, sentences=False)
	categories = tone["document_tone"].get('tone_categories')
	return categories
