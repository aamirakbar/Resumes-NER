import json
import re

def parse_text(data):
	text = data['content'].replace("\n", " ").replace("\t", " ")
	data_list = re.split('[\n,:]', text)
	data_list = [re.sub('[^A-Za-z0-9+# ]+', '', data).strip() \
						for data in data_list if data != '']
	data = ' '.join(x for x in data_list)
	return data

def clean_data(Data_File_Path):
	try:
		clean_data = []
		lines=[]
		with open(Data_File_Path, 'r') as f:
			lines = f.readlines()
			for line in lines:
				data = json.loads(line)
				text = parse_text(data)
				print(type(text))
				break

	except Exception as e:
		print(e)
        #return None

clean_data("dataset/Entity_Recognition_in_Resumes.json")
