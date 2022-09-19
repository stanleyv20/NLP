import spacy
from spacy import displacy

# loading a model
nlp = spacy.load('en_core_web_md')

text = 'Although my wise friends advised me, I still decided to not invest in cryptocurrency'

# creating a spacy object
doc = nlp(text)

# extracting noun phrases
noun_phrases = [chunk.text for chunk in doc.noun_chunks]
print(f'NOUN PHRASES: {noun_phrases}')

# get verbs
verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
print(f'VERBS: {verbs}')

# Named Entity Recognition
for entity in doc.ents:
    print(entity.text, entity.label_)

# output dependency
for token in doc:
    print(token, token.dep_)


displacy.render(doc, style='dep')
for sentence in doc.sents:
    displacy.render(sentence, style='dep')