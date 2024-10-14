import csv
import json
import os

def load_mountain_names(csv_file):
    mountain_names = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # To ensure no empty lines are processed
                mountain_names.append(row[0].strip())
    return mountain_names

def is_overlapping(new_annotation, existing_annotations):
    new_start, new_end = new_annotation[0], new_annotation[1]  # Беремо тільки початок і кінець
    for existing_annotation in existing_annotations:
        existing_start, existing_end = existing_annotation[0], existing_annotation[1]  # Беремо тільки початок і кінець
        if (new_start < existing_end and new_end > existing_start):
            return True
    return False

def annotate_text(text, mountain_names):
    annotations = []
    for mountain in mountain_names:
        start_idx = text.find(mountain)
        while start_idx != -1:
            end_idx = start_idx + len(mountain)
            new_annotation = [start_idx, end_idx]  # Додаємо тільки початок і кінець

            # Check for overlap before adding
            if not is_overlapping(new_annotation, annotations):
                annotations.append(new_annotation + ["MOUNTAIN"])  # Додаємо мітку тільки при додаванні

            start_idx = text.find(mountain, end_idx)
    return annotations

def process_text_file(txt_file, mountain_names):
    with open(txt_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    annotations = annotate_text(text, mountain_names)
    return [text, {"entities": annotations}]

def append_to_json(output_file, new_data):
    # Check if the file exists and is not empty
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, 'r+', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)  # Attempt to load existing data
            except json.JSONDecodeError:
                existing_data = []  # If loading fails, assume the file is empty or corrupted
            existing_data.append(new_data)
            f.seek(0)
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
    else:
        # If the file doesn't exist or is empty, create a new one
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump([new_data], f, ensure_ascii=False, indent=2)

def main(txt_file, csv_file, output_file):
    # Load mountain names from the CSV file
    mountain_names = load_mountain_names(csv_file)
    
    # Process the text file and generate annotations
    new_annotation = process_text_file(txt_file, mountain_names)
    
    # Append the new annotation to the JSON file
    append_to_json(output_file, new_annotation)

if __name__ == "__main__":
    txt_file = r'D:\(NER) model for the identification of mountain names\NER_python_annotation\train_data\mountain_text_train.txt'  # Replace with your text file
    csv_file = r'D:\(NER) model for the identification of mountain names\NER_python_annotation\train_data\mount_dataset.csv'  # Replace with your CSV file
    output_file = r'D:\(NER) model for the identification of mountain names\NER_python_annotation\train_data\annotations.json'  # Replace with your desired output file

    main(txt_file, csv_file, output_file)
