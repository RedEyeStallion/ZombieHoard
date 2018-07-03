#!/usr/bin/env python3

# Ryan Hodgson
# hodgson@csu.fullerton.edu
# This file implements the class MyPRNG to generate pseudo-random numbers

class MyPRNG:
	'Lehmer Generator'

	def __init__(self):
		self.m = 2147483647
		self.a = 16807

	def next_prn(self):
		self.seed = (self.a * self.seed) % self.m
		return(self.seed)

	def setSeed(self, rseed):
		self.seed = int(rseed)
