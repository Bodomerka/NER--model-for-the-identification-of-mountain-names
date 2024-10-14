import json

def convert_format(input_file, output_file):
    # Читаємо початковий JSON файл
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Отримуємо список анотацій
    annotations = data.get("annotations", [])
    
    # Новий формат даних
    new_format = []
    
    # Конвертуємо кожну анотацію
    for annotation in annotations:
        if annotation and isinstance(annotation, list) and len(annotation) >= 2:
            text = annotation[0]
            entities = annotation[1].get("entities", [])
            
            # Створюємо новий запис
            new_format.append([text, {"entities": entities}])
        else:
            print(f"Пропущено некоректну анотацію: {annotation}")
    
    # Записуємо дані у новий JSON файл
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_format, f, ensure_ascii=False, indent=2)

# Використання функції
input_file = r'D:\Tets_task1\data\annotations (4).json'  # Використання сирого рядка
output_file = r'D:\Tets_task1\data\outpu_m2.json'
convert_format(input_file, output_file)
