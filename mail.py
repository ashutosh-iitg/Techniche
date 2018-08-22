import pandas as pd
from validate_email import validate_email
import requests
import json
from enum import Enum


class ApiClient:
	apiUri = 'https://api.elasticemail.com/v2'
	apiKey = '01f87352-d942-4d6f-83f3-8201cbdae2b9'

	def Request(method, url, data):
		data['apikey'] = ApiClient.apiKey
		if method == 'POST':
			result = requests.post(ApiClient.apiUri + url, params = data)
		elif method == 'PUT':
			result = requests.put(ApiClient.apiUri + url, params = data)
		elif method == 'GET':
			attach = ''
			for key in data:
				attach = attach + key + '=' + data[key] + '&' 
			url = url + '?' + attach[:-1]
			result = requests.get(ApiClient.apiUri + url)	
			
		jsonMy = result.json()
		
		if jsonMy['success'] is False:
			return jsonMy['error']
			
		return jsonMy['data']

def Send(subject, EEfrom, fromName, to, bodyHtml, bodyText, isTransactional):
	return ApiClient.Request('POST', '/email/send', {
		'subject': subject,
		'from': EEfrom,
		'fromName': fromName,
		'to': to,
		'bodyHtml': bodyHtml,
		'bodyText': bodyText,
		'isTransactional': isTransactional})


if __name__ == "__main__":
    
    file = input("Enter input csv file: \n")
    data = pd.read_csv(file,sep=",")
    
    subject = input("Enter subject: \n")
    sender = input("Enter sender's address(your_event@techniche.org) : \n")
    
    #You can use html tags for proper punctuation. The file should still be .txt.
    fo = open(input("Enter Body file(.txt): \n")) 
    body = fo.read()
    #print(body)
    
    n = len(data)
    mail_id = data['email'][:]
    for i in range(n):
        if validate_email(mail_id[i]) is True:
            Send(subject, sender, "Techniche, IIT Guwahati", mail_id[i], body, "Text Body", True)
            #print(mail_id[i])
        else:
            print("Could not send to '", mail_id[i], "'. Invalid email address.")
    fo.close()


	#print(Send("Your Subject", "info@techniche.org", "Techniche, IIT Guwahati", "ashutoshk167@gmail.com", "<h1>Hey Ashutosh</h1>", "Text Body", True))


