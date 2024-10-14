import json
import spacy

def load_validation_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        validation_data = json.load(f)
    return validation_data

def extract_entities(annotation):
    entities = []
    for ent in annotation['entities']:
        start, end, label = ent
        entities.append((start, end, label))
    return entities

def evaluate_model(nlp, text, true_entities):
    # Predict entities using the model
    doc = nlp(text)
    
    # Get predicted entities
    predicted_entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
    
    # Print predicted entities
    print("Predicted Entities:")
    print(predicted_entities)
    
    # Print true entities
    print("True Entities:")
    print(true_entities)
    
    # Convert lists to sets for comparison
    true_set = set(true_entities)
    pred_set = set(predicted_entities)
    
    # Calculate TP, FP, FN
    tp = len(true_set & pred_set)
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)
    
    # Calculate Precision, Recall, F1-Score
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # Print metrics
    print("\nMetrics for the current text:")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    # Return metrics for further use
    return tp, fp, fn

def main():
    # Path to the validation file with annotations
    validation_file_path = r'D:\(NER) model for the identification of mountain names\model_evaluation\valid.json'
    
    # Load the validation file
    validation_data = load_validation_file(validation_file_path)
    
    # Load the trained spaCy model
    model_path = r"D:\(NER) model for the identification of mountain names\NER_python_annotation\output_model"
    nlp = spacy.load(model_path)
    
    # Variables to accumulate metrics for the entire dataset
    total_tp = 0
    total_fp = 0
    total_fn = 0
    
    # For each text in the file
    for sample in validation_data:
        text = sample[0]
        annotation = sample[1]
        
        # Extract true entities from annotations
        true_entities = extract_entities(annotation)
        
        print("\nText for evaluation:")
        print(text)
        
        # Evaluate the model for the current text
        tp, fp, fn = evaluate_model(nlp, text, true_entities)
        
        # Accumulate metrics
        total_tp += tp
        total_fp += fp
        total_fn += fn
    
    # Calculate overall metrics
    overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    overall_f1 = 2 * overall_precision * overall_recall / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0.0
    
    print("\nOverall metrics for the entire dataset:")
    print(f"Overall Precision: {overall_precision:.4f}")
    print(f"Overall Recall: {overall_recall:.4f}")
    print(f"Overall F1-Score: {overall_f1:.4f}")

if __name__ == "__main__":
    main()
