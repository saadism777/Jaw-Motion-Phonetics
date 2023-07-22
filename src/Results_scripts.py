import os
import csv

def process_output_directory(output_dir):
    rows = []
    
    # Get the absolute path to the "outputs" directory
    output_dir = os.path.abspath(output_dir)
    
    # Loop through all folders in the "outputs" directory
    for root_folder in os.listdir(output_dir):
        root_folder_path = os.path.join(output_dir, root_folder)
        
        # Check if it's a directory and if it contains "audio" subfolder
        if os.path.isdir(root_folder_path):
            audio_folder_path = os.path.join(root_folder_path, 'audio')
            
            # Check if "audio" subfolder exists
            if os.path.exists(audio_folder_path):
                row = {'Root Folder Name': root_folder}
                
                # Loop through the six folders inside "audio"
                for folder_name in ['bilabial', 'fricative', 'linguodental', 'mixed', 'sibilant']:
                    folder_path = os.path.join(audio_folder_path, folder_name)
                    stats_file_path = os.path.join(folder_path, f'{folder_name}_statistics.txt')
                    
                    # Initialize mean and variance as None
                    mean = None
                    variance = None
                    
                    # Try to read data from the stats file
                    try:
                        with open(stats_file_path, 'r') as stats_file:
                            lines = stats_file.readlines()
                            mean = lines[0].strip().split(': ')[1]
                            variance = lines[1].strip().split(': ')[1]
                    except FileNotFoundError:
                        pass
                    
                    # Store data in the row dictionary
                    row[f'{folder_name.capitalize()} Mean'] = mean
                    row[f'{folder_name.capitalize()} Variance'] = variance
                
                # Append the row to the rows list
                rows.append(row)
    
    # Write the data to a CSV file
    csv_file_path = os.path.join(output_dir, 'output_data.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Root Folder Name', 'Bilabial Mean', 'Bilabial Variance', 
                      'Fricative Mean', 'Fricative Variance', 'Linguodental Mean', 'Linguodental Variance', 
                      'Mixed Mean', 'Mixed Variance', 'Sibilant Mean', 'Sibilant Variance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Replace 'outputs' with your desired directory path, which is one directory up from the script location
output_directory = '../outputs'
process_output_directory(output_directory)
