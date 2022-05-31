import json
import re
import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding

def train_data():

	try:
		training_data = []
		with open("clean_data/clean_data.json", 'r') as f:
			for line in f.readlines():
				data = json.loads(line)
				text = data['content']
				entities = []
				for annotation in data['annotation']:
					point = annotation['points'][0]
					labels = annotation['label']
					if not isinstance(labels, list):
						labels = [labels]
					for label in labels:
						entities.append((point['start'], point['end'] + 1 ,label))
				training_data.append((text, {"entities" : entities}))

			return training_data

	except Exception as e:
		print(e)
		return None

def entity_spans(data):
	invalid_span_tokens = re.compile(r'\s')

	train_data = []
	for text, annotations in data:
		entities = annotations['entities']
		valid_entities = []
		for start, end, label in entities:
			if label == "Skills" or label == "Degree" or label == "Designation":
				valid_start = start
				valid_end = end
				while valid_start < len(text) and invalid_span_tokens.match(
                        text[valid_start]):
					valid_start += 1
				while valid_end > 1 and invalid_span_tokens.match(
                        text[valid_end - 1]):
					valid_end -= 1
				valid_entities.append([valid_start, valid_end, label])
			train_data.append([text, {'entities': valid_entities}])

	return train_data

def train_ner_model(train_data):

	if 'ner' not in nlp.pipe_names:
		ner = nlp.create_pipe('ner')
		nlp.add_pipe('ner', last=True)
       
	for _, annotations in train_data:
		for ent in annotations.get('entities'):
			ner.add_label(ent[2])

	other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
	with nlp.disable_pipes(*other_pipes):
		optimizer = nlp.begin_training()
		losses = {}
		batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
		k = 1
		for batch in batches:
			print("Iteration = ", k)
			for text, annotations in batch:
				try:
					doc = nlp.make_doc(text)
					example = Example.from_dict(doc, annotations)
					nlp.update([example], losses=losses, drop=0.5)
				except Exception as e:
					pass

			print(losses)
			k+=1
			if k==100:
				break;
	

data = train_data()
train_data = entity_spans(data)

nlp = spacy.blank('en')
train_ner_model(train_data)
nlp.to_disk('nlp_model')

