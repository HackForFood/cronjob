#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys, tweepy, unirest, datetime
import hashlib
import time
from apscheduler.schedulers.blocking import BlockingScheduler
HASHTAG="#H4G15VA"
reload(sys)
sys.setdefaultencoding("utf8")

consumer_key="khjuNY28wk3qx26cgO3d4VLol"
consumer_secret="F1AhwUzDuTBv4MMYpff0l7MiVRF6q9IYmKhZH7jykryZuObexq"
access_key = "3175655548-fCgIySiy6KJhfSEkbQiYEh4wm7xyUeYwgLi9r8K"
access_secret = "P4Sjlc3nICtdSDX0c1WYiOkBrBJmMWkjmXfdSfzMdyLdt"
banks = unirest.get("http://46.101.179.35/banco-alimentos").body
sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=12)
def fetch():
	for banco in unirest.get("http://46.101.179.35/banco-alimentos").body:
		necesidades = obtenerNecesidades(banco.get('id'))
		if len(necesidades) > 0:
			tweet=generarTweet(banco,necesidades)
			print tweet
			post(tweet)
			
		
def obtenerNecesidades(idBanco):
	necesidades=[]
	
	demands = unirest.get("http://46.101.179.35/demandas").body
	print demands
	for recurso in demands:
		if recurso.get('esNecesario') and recurso.get('idBancoAlimentos') == idBanco:
			necesidades.append(recurso.get('demanda'))
	return necesidades
	
def generarTweet(banco,necesidades):
	mensaje="""
		%s %s %s, %s,%s, necesitan %s
	"""%(HASHTAG,time.strftime("%d/%m/%y"),generarURL(banco.get('id')),banco.get('nombre'),banco.get('provincia'),", ".join(necesidades))
	if len(mensaje) > 140:
		mensaje = str(mensaje[0:137]) + str("...")
	print mensaje[:140]
	return mensaje[:140]
		
	
		
def obtenerBanco(idBanco):
	salida = -1
	for banco in unirest.get("http://46.101.179.35/banco-alimentos").body:
		if banco.get('id') == idBanco:
			salida = banco
	return salida
	
def generarURL(idBanco):
	return "https://fast-anchorage-9032.herokuapp.com/banco/"+idBanco
			

def post(data):
	try:
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_key, access_secret)
		api = tweepy.API(auth)
		api.update_status(status=data)
	except:
		pass
fetch()
sched.start()
