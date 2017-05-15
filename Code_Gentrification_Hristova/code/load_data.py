import csv
import datetime

class MontrealDataLoader:

	def __init__(self):

		self.load_venues()
		self.load_users_to_venues()

	def load_venues(self):
		#venue_id, coords, type, checkins, users, name, neighbourhood
		self.venues = {}
		f = csv.reader(open('../data/neighbourhood_venues.csv'))
		f.next()
		for line in f:
			self.venues[line[1]] = tuple(line[2:11])

	def load_users_to_venues(self):
		#user_id, venue_id, datetime
		self.venues_to_users = {}
		self.users_to_venues = {}
		with open('../data/montreal_trajectories_newcrawl.txt') as f:
			for line in f:
				splits = line.split('*;;;;*')
				user_id = int(splits[0])
				info = eval(splits[1])
				for c in info:
					venue = c[0]
					self.venues_to_users.setdefault(venue, set())
					self.users_to_venues.setdefault(user_id,set())
					self.venues_to_users[venue].add(user_id)
					self.users_to_venues[user_id].add(venue)
				





