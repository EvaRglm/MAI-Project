import os
import json
import shutil

def extract_filenames_and_img_ids(directory):
    # Specify the directory containing the images
    directory = 'GLIP/DATASET/coco/val2017'

    # Get a list of all files in the directory
    all_img_files = os.listdir(directory)

    # Get the first n files
    img_files = all_img_files[:5]
    img_ids = [int(img_file.replace('0','').replace('.jpg','')) for img_file in img_files]
    print(img_ids)

    return img_files, img_ids


def copy_specific_files(src_dir, dst_dir, img_files):
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


def extract_elements_from_json(json_data, img_ids):
    # Extract info, licenses, and categories
    info = json_data.get('info', {})
    licenses = json_data.get('licenses', [])
    categories = json_data.get('categories', [])
    
    # Extract images and annotations with the specific image ids
    filtered_images = [image for image in json_data.get('images', []) if image.get('id') in img_ids]
    filtered_annotations = [annotation for annotation in json_data.get('annotations', []) if annotation.get('image_id') in img_ids]
    
    return {
        'info': info,
        'licenses': licenses,
        'images': filtered_images,
        'annotations': filtered_annotations,
        'categories': categories
    }

# extract filenames and image ids
img_dir = 'GLIP/DATASET/coco/val2017'
img_files, img_ids = extract_filenames_and_img_ids (img_dir)

# extract specific image files
dst_dir = 'val2017_filtered'
copy_specific_files(img_dir, dst_dir, img_files)

# extract specific image annotations
input_file_path = 'GLIP/DATASET/coco/annotations/instances_val2017.json'
output_file_path = 'instances_val2017_filtered.json'

with open(input_file_path, 'r') as file:
    json_data = json.load(file)

filtered_data = extract_elements_from_json(json_data, img_ids)

with open(output_file_path, 'w') as outfile:
    json.dump(filtered_data, outfile, indent=2)