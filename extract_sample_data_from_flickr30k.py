import os
import json
import shutil
import regex as re

def extract_elements_from_json(json_data, n):
    # Extract info, licenses, and categories
    info = json_data.get('info', {})
    licenses = json_data.get('licenses', [])
    categories = json_data.get('categories', [])
    
    # Extract images and annotations with the specific image ids
    filtered_image_files = list(dict.fromkeys([img.get('file_name') for img in json_data.get('images', [])]))[:n]
    filtered_images = [image for image in json_data.get('images', []) if image.get('file_name') in filtered_image_files]
    filtered_image_ids = [img.get('id') for img in filtered_images]
    filtered_annotations = [annotation for annotation in json_data.get('annotations', []) if annotation.get('image_id') in filtered_image_ids]

    return filtered_image_files, {
        'info': info,
        'licenses': licenses,
        'images': filtered_images,
        'annotations': filtered_annotations,
        'categories': categories
    }

def copy_specific_files(src_dir, dst_dir, img_files_path):
    # Read image file names/teamspace/studios/this_studio/GLIP/docs
    with open(img_files_path) as file_d:
        img_files = [line.strip() for line in file_d]
    img_files = [img_file+'.jpg' for img_file in img_files]
    print(img_files)

    # Ensure the destination folder exists
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    
    # List files in the source folder
    for file_name in os.listdir(src_dir):
        # Check if the file name is in img_files list
        if file_name in img_files:
            # Construct full file path
            src_file_path = os.path.join(src_dir, file_name)
            dst_file_path = os.path.join(dst_dir, file_name)
            
            # Copy the file to the destination folder
            shutil.copy2(src_file_path, dst_file_path)
            print(f"Copied {file_name} to {dst_dir}")

def save_file_names(file_path, image_files):
    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Write each element on a new line
        for element in image_files:
            file.write(f"{element}\n")


def main():
    # # extract specific image annotations
    # n = 10
    # input_file_path = 'DATASET_b/OpenSource/final_flickr_separateGT_val.json'
    # output_file_path = 'DATASET/mdetr_annotations/final_flickr_separateGT_val.json'

    # with open(input_file_path, 'r') as file:
    #     json_data = json.load(file)

    # filtered_image_files, filtered_data = extract_elements_from_json(json_data, n)

    # with open(output_file_path, 'w') as outfile:
    #     json.dump(filtered_data, outfile, indent=2)

    # extract specific image files
    src_dir = 'DATASET/flickr30k/flickr30k_images'
    dst_dir = 'DATASET/flickr30k/flickr30k_images/test'
    img_files_path = 'DATASET/flickr30k/flickr30k/test.txt'
    copy_specific_files(src_dir, dst_dir, img_files_path)

    # # write image file names to a file
    # file_path = 'DATASET/flickr30k/flickr30k/test.txt'
    # save_file_names(file_path, filtered_image_files)

if __name__ == '__main__':
    main()