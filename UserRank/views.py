from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import json
import time
from pathlib import Path
import os
import numpy as np
import tweepy
from . import findUser
from memory_profiler import profile
import secrets


class InputPageView(TemplateView):
    def get(self, request, **kwargs): 
    	twitter_logo = os.path.join(settings.BASE_DIR, 'twitter-icon.jpg')
    	print(twitter_logo)
    	context={ 'logo': twitter_logo}
    	return render(request, 'input.html', context)

class OutputPageView(TemplateView):
	def get(self,request,**kwargs):
		consumer_key = request.GET.get('ckey')
		consumer_secret = request.GET.get('cskey')
		access_token = request.GET.get('atkey')
		access_token_secret = request.GET.get('atskey')
		username = request.GET.get('id')
		count = int(request.GET.get('count'))

		findUser.run(username, consumer_key, consumer_secret, access_token, access_token_secret)
		json_data = open(os.path.join(settings.BASE_DIR, 'sortedAccounts.json'))
		print(os.path.join(settings.BASE_DIR, 'sortedAccounts.json'))
		twitter_logo = os.path.join(settings.BASE_DIR, 'twitter-icon.png')
		UserJson = json.load(json_data)
		print(UserJson[1][1]['name'])
		print(twitter_logo)
		context = {
			'user':UserJson[:count],
			'range':range(0,3),
			'logo': twitter_logo,
			'myname': request.GET.get('id')
		}
		return render(request, 'output.html', context)