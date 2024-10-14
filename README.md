# **(NER) model for the identification of mountain names inside the texts.**



---
## Overview

---

This project focuses on recognizing mountain names in text using named object recognition (NER) and neural networks. The goal is to extract mountain names from text data.


---
## Data Collection


---

The data was generated using GPT chat.

The data was annotated in two ways:



*   By automatic annotation, using a method of searching for mountain names in the text, and by specifying labels in the annotated data.
*   Manual annotation, using the data annotation service for spaCy models

---
## Model Training


---


*   To train mountain recognition in text, we used free open-source library for Natural Language Processing - **spaCy**.
*The data were annotated according to the requirements of spaCy
*   The models were set up with the same parameters except for the number of training epochs. For the manually annotated data, **25 epochs** were set, and for the model trained with automatically annotated data, **35 epochs** were specified.



---
## Model Inference


---
* We used trained models for output.
The models predicted the names of the mountains in the input text.


---
## Usage


---
First, choose the model you want to use


1.   NER_manual_annotation (F1-Score: **0.7857**)
2.   NER_python_annotation (F1-Score: **0.6542**)

* Upload your text to **data_example.txt**
* Run **interface.py**
The console will display 

1. A list of entities found by the model and labels where they are located
2. General text in which entities will be highlighted on both sides with “**”
