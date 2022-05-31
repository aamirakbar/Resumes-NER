# Resumes-NER
Read resumes from a 'dataset/Entity_Recognition_in_Resumes.json'. Clean text in resumes. Train NER model and score resumes in Testing, Development, and Management categories.

# Usage

I recomment using virtual environment for Python.

python3.8 -m venv <name_of_venv>

# Activate the virtual environment (Unix):
source <name_of_venv>/bin/activate

pip3 install spacy

# Prepare the Data

1. run python clean_data.py

2. This will update the clean_data.json file in the clean_data folder

# Train NER model

1. run python train_model.py

2. This will save the NER model in current directory location

# Score Resume

1. Open jupyter notebook: score_resumes.ipynb

2. Run notebook: you will see a table at the end
