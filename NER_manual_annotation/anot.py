import json

def convert_format(input_file, output_file):
    # Read the initial JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get the list of annotations
    annotations = data.get("annotations", [])
    
    # New data format
    new_format = []
    
    # Convert each annotation
    for annotation in annotations:
        if annotation and isinstance(annotation, list) and len(annotation) >= 2:
            text = annotation[0]
            entities = annotation[1].get("entities", [])
            
            # Create a new entry
            new_format.append([text, {"entities": entities}])
        else:
            print(f"Skipped invalid annotation: {annotation}")
    
    # Write the data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_format, f, ensure_ascii=False, indent=2)

# Usage of the function
input_file = r'D:\(NER) model for the identification of mountain names\NER_manual_annotation\train_data\raw_annotations.json'  # Use of raw string
output_file = r'D:\(NER) model for the identification of mountain names\NER_manual_annotation\train_data\annotations.json'
convert_format(input_file, output_file)
