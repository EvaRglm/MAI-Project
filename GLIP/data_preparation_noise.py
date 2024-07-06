import os
import re
import cv2
import xml.etree.ElementTree as ET
import re
import numpy as np
import random




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


def add_salt_and_pepper_noise(image_path, max_bbox, output_folder, image_id, salt_prob=0.4, pepper_prob=0.4):
    image = cv2.imread(image_path)
    if image is not None:
    # x, y, w, h = coords
        xmin, ymin, xmax, ymax = max_bbox
        w = np.abs(xmax-xmin)
        h = np.abs(ymax-ymin)
        noisy_part = image[ymin:ymax, xmin:xmax]
        total_pixels = w * h
        num_salt = np.ceil(salt_prob * total_pixels)
        num_pepper = np.ceil(pepper_prob * total_pixels)
    
        # Add salt noise (white pixels)
        for _ in range(int(num_salt)):
            i = random.randint(0, h-1)
            j = random.randint(0, w-1)
            noisy_part[i, j] = 255

        # Add pepper noise (black pixels)
        for _ in range(int(num_pepper)):
            i = random.randint(0, h-1)
            j = random.randint(0, w-1)
            noisy_part[i, j] = 0

        image[ymin:ymax, xmin:xmax] = noisy_part
        output_filename = os.path.join(output_folder, f'output_{image_id}.jpg')
        cv2.imwrite(output_filename, image)
        print(f"Processed {image_id} and saved as {output_filename}")
    



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
        image_gaussian_noise = add_salt_and_pepper_noise(image_path, max_bbox, output_folder, image_id)


def draw_bounding_box(image_path, bboxes, output_folder, image_id):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Image {image_path} not found.")
        return
        
    for bbox in bboxes:
        xmin, ymin, xmax, ymax = bbox
        color = (0, 255, 0)  # Green
        thickness = 2
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)

    output_filename = os.path.join(output_folder, f'output_{image_id}.jpg')
    cv2.imwrite(output_filename, image)
    print(f"Processed {image_id} and saved as {output_filename}")

if __name__ == "__main__":
    """image_folder = 'DATASET/flickr30k/flickr30k_images/test'
    sentence_folder = os.path.join('DATASET/flickr30k/flickr30k', 'Sentences')
    annotation_folder = os.path.join('DATASET/flickr30k/flickr30k', 'Annotations')
    output_folder = 'output_images_noised_10' """
    image_folder = '/teamspace/studios/this_studio/IMAGES_ATTACK/10_images_original'
    sentence_folder = os.path.join('/teamspace/studios/this_studio/PREDICTIONS_ATTACK/10_images_original', 'Sentences')
    annotation_folder = os.path.join('/teamspace/studios/this_studio/PREDICTIONS_ATTACK/10_images_original', 'Annotations')
    output_folder = 'output_images_noised_10'


    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_images(image_folder, sentence_folder, annotation_folder, output_folder) #giving all the necessary folders
