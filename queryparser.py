import spacy

#dictionary for languages
language_dict = {'en': 'en_core_web_sm'}

def get_keywords(query:str, language = None) -> list:
	"""Convert query into keywords

	query - string to extract keywords from
	language - (default None) string for SpaCy language model to use 

	>>> test_query = "About to start Radiation ... Need advice on what to expect"
	>>> keywords = get_keywords(test_query)
	>>> 'radiation' in keywords
	True
	>>> 'advice' in keywords
	True
	>>> 'what' in keywords
	False
	"""
	if not language:
		#Language detection not implemented
		#language = id_language(query)

		language = language_dict['en']
		#NOTE: At some point should train SpaCy model on queries/posts related to Cancer

	nlp = spacy.load(language)

	doc = nlp(query)

	keywords = []
	candidate_pos = ['NOUN', 'PROPN', 'VERB']


	#Currently only filtering for nouns, proper nouns, and verbs and removing stop words
	#In future will want to create a better model for finding keywords

	for sent in doc.sents:
		keywords = []
		for token in sent:
			if token.pos_ in candidate_pos and not token.is_stop:
				keywords.append(token.lemma_.lower())
	return keywords
  
def id_language(string:str):
	"""Should take in a string query and output a detected language 
	in the form of english -> en, french -> fr, etc."""
	raise NotImplementedError


