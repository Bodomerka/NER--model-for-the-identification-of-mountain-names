import spacy
from spacy.training import Example, offsets_to_biluo_tags
from sklearn.model_selection import train_test_split
import json
from tqdm import tqdm

# Load a blank spaCy pipeline for English
nlp = spacy.blank("en")

# Add the NER component if it does not exist
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Load training data from the JSON file
with open(r'D:\(NER) model for the identification of mountain names\train_data\spacy_train_data.json', 'r', encoding='utf-8') as f:
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

# Add label(s) for the entities in the dataset, e.g., "MOUNTAIN"
for text, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Split the data into training and validation sets (85% training, 15% validation)
train_data, valid_data = train_test_split(TRAIN_DATA, test_size=0.15)

# Create examples for training and validation sets
train_examples = [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in train_data]
valid_examples = [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in valid_data]

# Hyperparameters for model training
batch_size = 4
n_iter = 25
learn_rate = 0.00005
decay = 0.01

# Initialize the optimizer and start training
optimizer = nlp.begin_training()

# Function to evaluate the model on validation data
def evaluate_model(nlp, examples):
    scorer = nlp.evaluate(examples)
    return scorer

# Train the model and display progress with hyperparameter adjustment
for i in range(n_iter):
    losses = {}
    batches = spacy.util.minibatch(train_examples, size=batch_size)
    
    # Adjust the learning rate after each iteration
    learn_rate *= (1.0 - decay)
    
    # Display training progress
    for batch in tqdm(batches, desc=f"Iteration {i+1}/{n_iter}"):
        nlp.update(batch, sgd=optimizer, losses=losses)
    
    print(f"Iteration {i+1}, Losses: {losses}")
    
    # Evaluate the model every iteration
    scorer = evaluate_model(nlp, valid_examples)
    print(f"Precision after iteration {i+1}: {scorer['ents_p']}")
    print(f"Recall after iteration {i+1}: {scorer['ents_r']}")
    print(f"F1-score after iteration {i+1}: {scorer['ents_f']}")

# Save the trained model to disk
output_dir = "D:/(NER) model for the identification of mountain names/output_model"
nlp.to_disk(output_dir)
print(f"Model saved to {output_dir}")
