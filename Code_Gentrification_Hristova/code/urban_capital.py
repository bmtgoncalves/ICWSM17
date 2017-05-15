from __future__ import division
from math import log
from load_data import MontrealDataLoader
import csv

def venue_cat_vecs(venues):

	hoods = {}
	for venue in venues: 
		cat = venues[venue][3] #top level category
		no_checkins = int(venues[venue][6])
		hood = venues[venue][8]
		hoods.setdefault(hood, {})

		hoods[hood].setdefault(cat, 0)
		hoods[hood][cat]+=no_checkins

		#hoods[hood]['total'] = sum(hoods[hood].values())

	return hoods

def colocation(usera,userb,user_vecs):
	#test if two users have been colocated more than twice
	venuesa = user_vecs[usera]
	venuesb = user_vecs[userb]
	coloc = venuesa.intersection(venuesb)
	if len(coloc) > 2:
		return 1
	return 0		


def social_capital(place_vecs,user_vecs,venues):
	#compute social capital per hood
	social = {}
	for venue in place_vecs:
		if venue in venues:
			colocs = 0
			hood = venues[venue][8]
			n = len(place_vecs[venue])
			if n > 3:
				hood_venues = list(place_vecs[venue]) 
				for visitora in range(0,n):
					for visitorb in range(visitora,n):
						if visitora is not visitorb:
							coloc = colocation(hood_venues[visitora],hood_venues[visitorb],user_vecs)
							colocs += coloc
				density = float(colocs/((n*(n-1))/2))
				redundancy = float(density*(n-1))
				efficiency = float((n-redundancy)/n)
				if hood in social:
					social[hood].append(round(efficiency,2))
				else: 
					social[hood] = [round(efficiency,2)]
	return social

def social_capital_venue(visitors,user_vecs):
	#compute social capital of a venue in the form [user_id,...]
	colocs = 0 #number of colocation links b/w visitors
	n = len(visitors) #number of visitors
	efficiency = None
	if n > 3:
		for visitor_a in range(0,n):
			for visitor_b in range(visitor_a,n):
				if visitor_a is not visitor_b: #for every pair of visitors
					#user_vecs is a dict of user_id:[venue_id,...]
					coloc = colocation(visitors[visitor_a],visitors[visitor_b],user_vecs)
					colocs += coloc

		density = float(colocs/((n*(n-1))/2))
		redundancy = float(density*(n-1))
		efficiency = float((n-redundancy)/n)

	return efficiency

def cultural_capital(hoods):
	#hoods[hood]:{'category':no_checkins}
	hood_cult = {}
	for hood in hoods:
		if 'Arts & Entertainment' in hoods[hood]:
			cult = hoods[hood]['Arts & Entertainment']
			total = sum(hoods[hood].values())
			hood_cult[hood] = float(cult/total)

	return hood_cult


def cat_entropy(hoods):
	#hoods[hood]:{'category':number of checkins...}
	hood_ent = {}
	for hood in hoods:
		ent = 0
		total = sum(hoods[hood].values())
		for cat in hoods[hood]:
			if total is not 0:
				prob = float(hoods[hood][cat]/total)				
				e = prob*log(prob,2)
				ent += e
		hood_ent[hood] = -round(ent,2)
	return hood_ent


dl = MontrealDataLoader()
#print venue_cat_vecs(dl.venues)

venues = dl.venues
venues_to_users = dl.venues_to_users
users_to_venues = dl.users_to_venues

soc = social_capital(venues_to_users,users_to_venues,venues) 
sp = cat_entropy(venue_cat_vecs(venues))
cult = cultural_capital(venue_cat_vecs(venues))



