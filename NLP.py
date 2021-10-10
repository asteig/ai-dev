import re

ENGLISH_NOUNS = open('data/english_nouns.txt').read().split('\n')

class NLP:

	# get all nouns from a text description... 
	# only works on room descriptions right now...
	def nouns(txt):
		# gotta use NLP really...
		all_nouns = []
		
		# TODO: keep descriptors?
		for word in re.findall(r'[\w]+', txt):
			# normalize
			word = word.lower()
			if word in ENGLISH_NOUNS and word not in all_nouns:
				all_nouns.append(word)
				continue
				
			# maybe plural?
			# catch -s
			word = word[0:-1]
			if word in ENGLISH_NOUNS and word not in all_nouns:
				all_nouns.append(word)
				
			# catch -es
			word = word[0:-1]
			if word in ENGLISH_NOUNS and word not in all_nouns:
				all_nouns.append(word)
				
			# catch -ies
			word = word[0:-1] + 'y'
			if word in ENGLISH_NOUNS and word not in all_nouns:
				all_nouns.append(word)
				
		return all_nouns
