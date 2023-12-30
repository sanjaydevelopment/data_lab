import re
import os
import matplotlib.pyplot as plt
import random

def detect_personal_information(file_content, pi_patterns):
    detected_elements = [label for label, pattern in pi_patterns.items() if pattern.search(file_content)]
    return detected_elements

def main(folder_path):
    pi_patterns = {
        'Phone Numbers': re.compile(r'\b(?:\d{3}[-.\s]?\d{3}[-.\s]?\d{4})\b'),
        'Email Addresses': re.compile(r'\b[\w.-]+@[\w.-]+\b'),
        'SSN': re.compile(r'^\d{3}-\d{2}-\d{4}$'),
        'DOB': re.compile(r'^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'),
        'Credit Card Numbers': re.compile(r'\b(?:\d[ -]*?){13,16}\b'),
        'CC Expiry Date': re.compile(r'^(0[1-9]|1[0-2])\/\d{2}$'),
        'Amount' : re.compile(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?')
    }

    total_files_processed = 0
    pi_elements_per_file = {} 

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                file_content = file.read()

                detected_elements = detect_personal_information(file_content, pi_patterns)

                pi_elements_per_file[filename] = detected_elements

                total_files_processed += 1


    colors = {label: f'#{random.randint(0, 0xFFFFFF):06x}' for label in pi_patterns.keys()}

    labels = list(pi_elements_per_file.keys())
    fig, ax = plt.subplots()
    for i, label in enumerate(labels):
        elements = pi_elements_per_file[label]
        width = 0.2 * len(elements)
        offset = -(width / 2) 
        for element in elements:
            color = colors[element]
            bar = ax.bar(i + offset, 1, color=color, width=width, align='edge')
            offset += width 
    legend_labels = [plt.Rectangle((0,0),1,1, color=colors[element]) for element in pi_patterns.keys()]
    ax.legend(legend_labels, pi_patterns.keys(), loc='upper left', bbox_to_anchor=(1,1))
    ax.set_ylabel('Sensitive Data Elements')
    ax.set_title('Sensitive Data Elements Detected in Each File')
    plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    folder_path = 'sample_data'
    main(folder_path)