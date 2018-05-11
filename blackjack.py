#!/usr/bin/python

import random

HIT = 1
STICK = 0

class BlackJack:

	cards = [1,2,3,4,5,6,7,8,9,10,10,10,10]

	def __init__(self, player_sum, dealer_shows, useable_ace):
		self.player_sum = player_sum
		self.dealer_shows = dealer_shows
		self.useable_ace = useable_ace

	def drawCard(self):
		return random.choice(self.cards)

	def dealersTurn(self):
		dealer_sum = self.dealer_shows
		if dealer_sum == 1:
			dealer_ace = True
			dealer_sum = 11
		else:
			dealer_ace = False
		
		while dealer_sum < 17:
			new_card = self.drawCard()
			dealer_sum = dealer_sum + new_card
			if dealer_sum > 21 and dealer_ace == True:
				dealer_sum = dealer_sum - 10
				dealer_ace = False
			elif new_card == 1 and dealer_sum + 10 < 22:
				dealer_sum = dealer_sum + 10
				dealer_ace = True
			
		if dealer_sum > 21:
			return [self.player_sum, self.dealer_shows, self.useable_ace, 1, True]
		if dealer_sum > self.player_sum:
			return [self.player_sum, self.dealer_shows,  self.useable_ace, -1, True]
		if self.player_sum > dealer_sum:
			return [self.player_sum, self.dealer_shows,  self.useable_ace, 1, True]
		if self.player_sum == dealer_sum:
			return [self.player_sum, self.dealer_shows,  self.useable_ace, 0, True]

	def step(self, action):
		if action == STICK:
			return self.dealersTurn()
		else:
			new_card = self.drawCard()
			self.player_sum = self.player_sum + new_card
			#check if useable ace
			if self.player_sum > 21 and self.useable_ace == True:
				self.player_sum = self.player_sum - 10
				self.useable_ace = False
			#new card is ace check if useable
			elif new_card == 1  and self.player_sum + 10 < 22:
				self.player_sum = self.player_sum + 10
				self.useable_ace = True
			
			if self.player_sum > 21:
				return [self.player_sum, self.dealer_shows,  self.useable_ace, -1, True]
			else:
				return [self.player_sum, self.dealer_shows,  self.useable_ace, 0, False]

class State:

	def __init__(self, player_sum, dealer_shows, useable_ace):
		self.player_sum = player_sum
		self.dealer_shows = dealer_shows
		self.useable_ace = useable_ace
		self.n_hit = 1
		self.n_stick = 1
		self.Q_hit_total = 0
		self.Q_stick_total = 0
		self.policy = STICK

	def update(self, reward, action):
		if action == STICK:
			self.n_stick = self.n_stick + 1
			self.Q_stick_total = self.Q_stick_total + reward
		else:
			self.n_hit = self.n_hit + 1
			self.Q_hit_total = self.Q_hit_total + reward
		
		if self.Q_hit_total / float(self.n_hit) > self.Q_stick_total / float(self.n_stick):
			self.policy = HIT	
		else:
			self.policy = STICK

def getStateIdx(player_sum, dealer_shows, usable_ace):
	return ((player_sum - 12) * 10  + dealer_shows) * 2 - usable_ace - 1

def monteCarloES(num_episodes = 500000):
	states = [State(i, j, l) for i in range(12, 22) for j in range(1, 11) for l in reversed(range(2))]
	for i in range(0, num_episodes):
		s = random.choice(states)
		bj = BlackJack(s.player_sum, s.dealer_shows, s.useable_ace)
		action = random.randint(0, 1)
		while True:
			player_sum, dealer_shows, useable_ace, reward, game_over = bj.step(action)
			s.update(reward, action)
			if game_over == False:
				s = states[getStateIdx(player_sum, dealer_shows, useable_ace)]
				action = s.policy
			else:
				break

	for s in states:
		if s.useable_ace == 0:
			print(s.dealer_shows, s.player_sum, s.policy)
			#print (s.dealer_shows, s.player_sum, s.policy, s.n_hit, s.Q_hit_total / float(s.n_hit) ,s.n_stick, s.Q_stick_total / float(s.n_stick))

monteCarloES()