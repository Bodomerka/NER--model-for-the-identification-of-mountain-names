import spacy
from spacy.training import Example, offsets_to_biluo_tags
from sklearn.model_selection import train_test_split
import json
from tqdm import tqdm
import random

nlp = spacy.blank("en")

# Add the NER component if it does not exist
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Load training data from the JSON file
with open(r'D:\(NER) model for the identification of mountain names\NER_python_annotation\train_data\annotations.json', 'r', encoding='utf-8') as f:
    TRAIN_DATA = json.load(f)

# Function to check and fix entity offsets
def check_alignment(data):
    aligned_data = []
    for text, annotations in data:
        doc = nlp.make_doc(text)
        entities = annotations["entities"]
        try:
            # Check if the annotations are correctly aligned with the text
            biluo_tags = offsets_to_biluo_tags(doc, entities)
            aligned_data.append((text, annotations))
        except Exception as e:
            print(f"Entity alignment error in text: {text}, {e}")
    return aligned_data

# Verify and align the training data
TRAIN_DATA = check_alignment(TRAIN_DATA)

# Initialize the blank English model
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner", last=True)

# Add labels to the NER component
for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Define hyperparameters
n_iter = 35
batch_size = 4
dropout = 0.01
learn_rate = 0.00005

# Start the training process
optimizer = nlp.begin_training()

for iteration in range(n_iter):
    print(f"Iteration {iteration + 1}/{n_iter}")
    losses = {}
    
    # Shuffle the training data to avoid learning order bias
    random.shuffle(TRAIN_DATA)
    
    # Create mini-batches of training data
    batches = spacy.util.minibatch(TRAIN_DATA, size=batch_size)
    
    for batch in tqdm(batches):
        texts, annotations = zip(*batch)
        examples = []
        
        # Create Example objects from text and annotations
        for i in range(len(texts)):
            examples.append(Example.from_dict(nlp.make_doc(texts[i]), annotations[i]))
        
        # Update the model with mini-batch examples
        nlp.update(
            examples,
            drop=dropout,
            losses=losses,
            sgd=optimizer
        )
    
    print(f"Losses at iteration {iteration + 1}: {losses}")

# Save the trained model to disk
output_dir = r"D:\(NER) model for the identification of mountain names\NER_python_annotation\output_model"
nlp.to_disk(output_dir)
print(f"Model saved to {output_dir}")
