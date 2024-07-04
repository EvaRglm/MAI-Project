import os
import json
import shutil
import regex as re

def extract_image_annotations(input_file_path, output_file_path , n, filtered_image_files=None):
    with open(input_file_path, 'r') as file:
        json_data = json.load(file)

    # Extract info, licenses, and categories
    info = json_data.get('info', {})
    licenses = json_data.get('licenses', [])
    categories = json_data.get('categories', [])
    
    # Extract images and annotations with the specific image ids
    if filtered_image_files == None:
        filtered_image_files = list(dict.fromkeys([img.get('file_name') for img in json_data.get('images', [])]))[:n]
    if "92679312.jpg" in filtered_image_files:
        filtered_image_files.remove("92679312.jpg")
    filtered_images = [image for image in json_data.get('images', []) if image.get('file_name') in filtered_image_files]
    filtered_image_ids = [img.get('id') for img in filtered_images]
    filtered_annotations = [annotation for annotation in json_data.get('annotations', []) if annotation.get('image_id') in filtered_image_ids]
    print(filtered_image_files)
    filtered_data = {
        'info': info,
        'licenses': licenses,
        'images': filtered_images,
        'annotations': filtered_annotations,
        'categories': categories
    }
    with open(output_file_path, 'w') as outfile:
        json.dump(filtered_data, outfile, indent=2)

    return filtered_image_files

def extract_image_files(input_file_dir, output_file_dir, filtered_image_files):
    # Ensure the destination folders exist
    if not os.path.exists(output_file_dir):
        os.makedirs(output_file_dir)
        
    # Remove filename ending
    filtered_image_files_without_ending = [file.split('.')[0] for file in filtered_image_files]

    # List files in the source folder
    for file_name in os.listdir(input_file_dir):
        # Remove filename ending
        file_name_without_ending = file_name.split('.')[0]
        # Check if the file name is in filtered_image_files_without_ending list
        if file_name_without_ending in filtered_image_files_without_ending:
            # Construct full file path
            input_file_path = os.path.join(input_file_dir, file_name)
            output_file_path = os.path.join(output_file_dir, file_name)
            
            # Copy the file to the destination folder
            shutil.copy2(input_file_path, output_file_path)
            print(f"Copied {file_name} to {output_file_dir}")

def save_file_names(file_path, filtered_image_files):
    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Write each element on a new line
        for element in filtered_image_files:
            element = element.replace('.jpg', '')
            file.write(f"{element}\n")

def read_and_save_filenames(input_file_path, output_file_path):
    # Read filenames
    filenames = os.listdir(input_file_path)
    filenames = [f for f in filenames if os.path.isfile(os.path.join(input_file_path, f))]

    # Wrtie filenames
    with open(output_file_path, 'w') as file:
        # Write each element on a new line
        for element in filenames:
            element = element.replace('.jpg', '')
            file.write(f"{element}\n")
    return filenames

def create_folder_structure():
    ### Create a subset Dataset with less datapoints
    folder_structure = [
    "DATASET/flickr30k/flickr30k",
    "DATASET/flickr30k/flickr30k_images/test",
    "DATASET/flickr30k/flickr30k_images/val",
    "DATASET/mdetr_annotations"
    ]

    # Create the folders
    for folder in folder_structure:
        os.makedirs(folder, exist_ok=True)

def create_dataset_structure():
    input_file_path = 'DATASET/flickr30k/flickr30k_images/test'
    output_file_path = 'DATASET/flickr30k/flickr30k/test.txt'
    filtered_image_files_t = read_and_save_filenames(input_file_path, output_file_path)

    input_file_path = 'DATASET/flickr30k/flickr30k_images/val'
    output_file_path = 'DATASET/flickr30k/flickr30k/val.txt'
    filtered_image_files_v = read_and_save_filenames(input_file_path, output_file_path)

    # Extract a subset of test image annotations
    n = 1000
    input_file_path = 'DATASET_b/mdetr_annotations/final_flickr_separateGT_test.json'
    output_file_path = 'DATASET/mdetr_annotations/final_flickr_separateGT_test.json'
    # filtered_image_files_t = ['1000092795.jpg']
    filtered_image_files_test = extract_image_annotations(input_file_path, output_file_path , n, filtered_image_files_t)

    # Extract a subset of valiation image annotations
    input_file_path = 'DATASET_b/mdetr_annotations/final_flickr_separateGT_val.json'
    output_file_path = 'DATASET/mdetr_annotations/final_flickr_separateGT_val.json'
    # filtered_image_files_v = ['1000092795.jpg']
    filtered_image_files_val = extract_image_annotations(input_file_path, output_file_path , n, filtered_image_files_v)

    filtered_image_files_all = filtered_image_files_test + filtered_image_files_val

    # # Extract a subset of test images
    # input_file_dir = 'DATASET_b/flickr30k/flickr30k_images'
    # output_file_dir = 'DATASET/flickr30k/flickr30k_images/test'
    # extract_image_files(input_file_dir, output_file_dir, filtered_image_files_test)

    # # Extract a subset of validation images
    # input_file_dir = 'DATASET_b/flickr30k/flickr30k_images'
    # output_file_dir = 'DATASET/flickr30k/flickr30k_images/val'
    # extract_image_files(input_file_dir, output_file_dir, filtered_image_files_val)

    # # Extract a subset of all images
    # input_file_dir = 'DATASET_b/flickr30k/flickr30k_images'
    # output_file_dir = 'DATASET/flickr30k/flickr30k_images'
    # extract_image_files(input_file_dir, output_file_dir, filtered_image_files_all)

    # Extract a subset of all Annotations
    input_file_dir = 'DATASET_b/flickr30k/flickr30k/Annotations'
    output_file_dir = 'DATASET/flickr30k/flickr30k/Annotations'
    extract_image_files(input_file_dir, output_file_dir, filtered_image_files_all)

    # Extract a subset of all Sentences
    input_file_dir = 'DATASET_b/flickr30k/flickr30k/Sentences'
    output_file_dir = 'DATASET/flickr30k/flickr30k/Sentences'
    extract_image_files(input_file_dir, output_file_dir, filtered_image_files_all)

    # Safe the subset of test image filenames
    file_path = 'DATASET/flickr30k/flickr30k/test.txt'
    save_file_names(file_path, filtered_image_files_test)

    # Safe the subset of val image filenames
    file_path = 'DATASET/flickr30k/flickr30k/val.txt'
    save_file_names(file_path, filtered_image_files_val)

def main():
    # create_folder_structure()
    # Copy changed test images into the folders: DATASET/flickr30k/flickr30k_images/test, DATASET/flickr30k/flickr30k_images
    # Copy changed val images into the folders: DATASET/flickr30k/flickr30k_images/val, DATASET/flickr30k/flickr30k_images
    create_dataset_structure()

if __name__ == '__main__':
    main()