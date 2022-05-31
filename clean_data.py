import json
import re

def parse_text(data):
	text = data['content'].replace("\n", " ").replace("\t", " ")
	data_list = re.split('[\n,:]', text)
	data_list = [re.sub('[^A-Za-z0-9+# ]+', '', data).strip() \
						for data in data_list if data != '']
	data['content'] = ' '.join(x for x in data_list)

def clean_data(Data_File_Path):
	try:
		clean_data_writer = open("clean_data/clean_data.json", 'a')
		with open(Data_File_Path, 'r') as f:
			for line in f.readlines():
				data = json.loads(line)
				parse_text(data)
				json.dump(data, clean_data_writer)
				clean_data_writer.write("\n")

		clean_data_writer.close()
		return True

	except Exception as e:
		print(e)
		return False

if clean_data("dataset/Entity_Recognition_in_Resumes.json"):
	print("Data Cleaning successful")
	print("Clean Data stored in clean_data/clean_data.json")
