import os
import re
import cv2
import xml.etree.ElementTree as ET
import re
import numpy as np
import random

import os
import cv2
import numpy as np
import random



# remove black background in the images of objects
def remove_black_background(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create a binary mask where black pixels are considered background
    _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Invert the mask
    mask_inv = cv2.bitwise_not(mask)

    # Convert single channel mask to three channels
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask_inv_rgb = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2BGR)

    # Keep only the part of the image without the black background
    image_with_bg_removed = cv2.bitwise_and(image, mask_rgb)

    # Add alpha channel to the image
    b, g, r = cv2.split(image_with_bg_removed)
    rgba = [b, g, r, mask]
    image_with_alpha = cv2.merge(rgba, 4)

    return image_with_alpha
# function to insert the image of an object inside the bounding box
def insert_image(image, insert_image_path, bbox, percentage, start_margin):
    insert_img = cv2.imread(insert_image_path)
    if insert_img is None:
        print(f"Error: Image {insert_image_path} not found.")
        return image

    # Remove the black background
    insert_img = remove_black_background(insert_img)

    xmin, ymin, xmax, ymax = bbox
    bbox_width = xmax - xmin
    bbox_height = ymax - ymin

    if start_margin in ['top', 'bottom']:
        insert_width = bbox_width
        insert_height = int(bbox_height * (percentage / 100.0))
    elif start_margin in ['left', 'right']:
        insert_width = int(bbox_width * (percentage / 100.0))
        insert_height = bbox_height

    # Resize insert_img to fit the specified dimensions
    insert_img_resized = cv2.resize(insert_img, (insert_width, insert_height))

    # Determine the position to insert the image
    if start_margin == 'top':
        insert_y_start = ymin
        insert_x_start = xmin
    elif start_margin == 'bottom':
        insert_y_start = ymax - insert_height
        insert_x_start = xmin
    elif start_margin == 'left':
        insert_y_start = ymin
        insert_x_start = xmin
    elif start_margin == 'right':
        insert_y_start = ymin
        insert_x_start = xmax - insert_width

    # Handle alpha channel if present
    if insert_img_resized.shape[2] == 4:
        alpha_s = insert_img_resized[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            image[insert_y_start:insert_y_start+insert_height, insert_x_start:insert_x_start+insert_width, c] = (
                alpha_s * insert_img_resized[:, :, c] +
                alpha_l * image[insert_y_start:insert_y_start+insert_height, insert_x_start:insert_x_start+insert_width, c]
            )
    else:
        image[insert_y_start:insert_y_start+insert_height, insert_x_start:insert_x_start+insert_width] = insert_img_resized

    return image

def process_images_with_inserts(image_folder, sentence_folder, annotation_folder, insert_images_folder, percentage, start_margin, output_subfolder):
    bounding_boxes_data = dp.process_images(image_folder, sentence_folder, annotation_folder, output_subfolder)
    processed_images = []

    for image_path, bboxes, image_id in bounding_boxes_data:
        insert_images = [os.path.join(insert_images_folder, f) for f in os.listdir(insert_images_folder) if f.endswith('.png')]

        if not insert_images:
            print(f"No insert images found in folder: {insert_images_folder}")
            continue

        insert_image_path = random.choice(insert_images)

        # Draw bounding boxes and insert random image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Image {image_path} not found.")
            continue

        max_bbox = max(bboxes, key=dp.calculate_area)
        image_with_insert = insert_image(image, insert_image_path, max_bbox, percentage, start_margin)

        output_filename = os.path.join(output_subfolder, f'{image_id}.jpg')
        cv2.imwrite(output_filename, image_with_insert)
        print(f"Processed {image_id} and saved as {output_filename}")

        processed_images.append(image_with_insert)

    return processed_images

def extract_number_from_sentence(sentence_file):
    with open(sentence_file, 'r') as file:
        content = file.read()
        # numbers = [word.split('/')[0][4:] for word in content.split() if '/people' in word]
        numbers = re.findall(r'/EN#(\d+)/people', content)
        print(numbers)
        return numbers

def find_bounding_boxes(annotation_file, numbers):
    tree = ET.parse(annotation_file)
    root = tree.getroot()
    bboxes = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        if any(number in name for number in numbers):
            bndbox = obj.find('bndbox')
            if bndbox == None:
                print("none")
            else:
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                bboxes.append((xmin, ymin, xmax, ymax))
    print(bboxes)
    return bboxes

def calculate_area(bbox):
    xmin, ymin, xmax, ymax = bbox
    return (xmax - xmin) * (ymax - ymin)



def process_images(image_folder, sentence_folder, annotation_folder, output_folder):
    for image_filename in os.listdir(image_folder): #open the image
        if not image_filename.endswith('.jpg'):
            continue
        
        image_id = os.path.splitext(image_filename)[0] #take image name
        image_path = os.path.join(image_folder, image_filename)
        sentence_path = os.path.join(sentence_folder, image_id + '.txt') #find the paths
        annotation_path = os.path.join(annotation_folder, image_id + '.xml')

        if not os.path.exists(sentence_path) or not os.path.exists(annotation_path): #if there is a missing file skip this image
            print(f"Missing files for {image_id}")
            continue
        
        numbers = extract_number_from_sentence(sentence_path) #find the number for person tag
        
        bboxes = find_bounding_boxes(annotation_path, numbers) #find al the bounding boxes
        
        if not bboxes:
            print(f"No bounding boxes found for {image_id} with number") #if there is not a person tag skip the image
            continue
        
        max_bbox = max(bboxes, key=calculate_area) #calculate max bounding box
        #you can put the necessary work in here instead to the image with the bounding box
        # draw_bounding_box(image_path, bboxes, output_folder, image_id) 
        #image_gaussian_noise = add_salt_and_pepper_noise_down(image_path, max_bbox, output_folder, image_id)



if __name__ == "__main__":
    image_folder = 'DATASET/flickr30k/flickr30k_images/test'
    sentence_folder = os.path.join('DATASET/flickr30k/flickr30k', 'Sentences')
    annotation_folder = os.path.join('DATASET/flickr30k/flickr30k', 'Annotations')
    output_folder = 'output_images_noised_10'

   """ image_folder = '/teamspace/studios/this_studio/IMAGES_ATTACK/10_images_original'
    sentence_folder = os.path.join('/teamspace/studios/this_studio/PREDICTIONS_ATTACK/10_images_original', 'Sentences')
    annotation_folder = os.path.join('/teamspace/studios/this_studio/PREDICTIONS_ATTACK/10_images_original', 'Annotations')
    output_folder = 'output_images_noised_10_50percentleft'


    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    
    process_images(image_folder, sentence_folder, annotation_folder, output_folder) #giving all the necessary folders
    
    """
    percentage = 50
    start_margin = 'top'

    output_subfolder = os.path.join(output_base_folder, f'{start_margin}_{percentage}')
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)
    processed_images = process_images_with_inserts(image_folder, sentence_folder, annotation_folder, insert_images_folder, percentage, start_margin, output_subfolder)
    #plot_images(processed_images, f"{start_margin.capitalize()} {percentage}%")