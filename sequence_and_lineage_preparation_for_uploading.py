import os
import re
import csv

#Getting all the paths for fasta files in the file
input_directory = '/home/vaskaxxx/covid_assembly/upload_preparation/Input'
output_directory = '/home/vaskaxxx/covid_assembly/upload_preparationOutput'
file_paths = []

for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.endswith(".fasta"):
            file_paths.append(os.path.join(root, file))

#Changing all the fasta file headers to an appropriate format and saving to a new file
for fasta_file_path in file_paths:
    #Reading a file and creating modified lines
    with open(fasta_file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    #Extracting the MB number
    pattern = r">MB(\d+_\d+)"

    for line in lines:
        if line.startswith(">"):
            match = re.search(pattern, line)
            if match:
                sequence_id = match.group(1)
                modified_line = f">hCoV-19/Lithuania/MB{sequence_id}/2023\n"
                modified_lines.append(modified_line)
            else:
                modified_lines.append(line)
        else:
            modified_lines.append(line)
    
    new_fasta_file_path = ''
    pattern_name = r"\d{4}_\d{2}_\d{2}_VLN_NVSPL_r\d{2}_\d{2}"
    match = re.search(pattern_name, fasta_file_path)
    if match:
        extracted_part = match.group()
        new_fasta_file_path = os.path.join(os.getcwd(), 'Input', f'{extracted_part}.fasta')
    else:
        print("Can't modify fasta file name")

    #Creating a new file
    with open(new_fasta_file_path, 'w') as file:
        file.writelines(modified_lines)
    
    with open(new_fasta_file_path, 'r') as file:
        lines = file.readlines()

        converted_lines = []
        current_sequence = ""

        for line in lines:
            line = line.strip()
            if line.startswith(">"):
                if current_sequence:
                    converted_lines.append(current_sequence + "\n")
                    current_sequence = ""
                converted_lines.append(line + "\n")
            else:
                current_sequence += line

        if current_sequence:
            converted_lines.append(current_sequence + "\n")
    
    final_fasta_file_path = os.path.join('/home/vaskaxxx/covid_assembly/upload_preparation/Output', f'{extracted_part}.fasta')

    with open(final_fasta_file_path, 'w') as file:
        file.writelines(converted_lines)


# Generating a fasta_register from all of the final sequences
fasta_files_path_names = []

for root, dirs, files in os.walk(output_directory):
    for file in files:
        if file.endswith(".fasta"):
            fasta_files_path_names.append(os.path.join(root, file))

# Creating fasta registry and concatenating all fasta files
data = [['File name', 'Sequence header']]

for path in fasta_files_path_names:
    final_file_name = os.path.basename(path)

    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                header = line[1:]  # Remove the ">" symbol from the header
                data.append([final_file_name, header])



with open(os.path.join('/home/vaskaxxx/covid_assembly/upload_preparation/Output', f'fasta_registry.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)


output_file_path = os.path.join('/home/vaskaxxx/covid_assembly/upload_preparation/Output', f'concatenated_all_fastas.fasta')

with open(output_file_path, 'w') as output_file:
    for input_file in fasta_files_path_names:
        with open(input_file, 'r') as input_file:
            for line in input_file:
                output_file.write(line)