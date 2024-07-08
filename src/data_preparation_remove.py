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



def inpaint_image(image_path, bounding_boxes_to_remove, output_folder, image_id, percentage=0.50, side='top'):
    image = cv2.imread(image_path)
    # Extract bounding box coordinates
    xmin, ymin, xmax, ymax = bounding_boxes_to_remove
    w = xmax - xmin
    h = ymax - ymin
    #Creates a mask with the same dimensions as the image
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    
    # Calculate the dimensions of the area to be removed
    if side in ['top', 'bottom']:
        remove_height = int(h * percentage)
        if side == 'top':
            mask[ymin:ymin + remove_height, xmin:xmax] = 1
        elif side == 'bottom':
            mask[ymax - remove_height:ymax, xmin:xmax] = 1
    elif side in ['left', 'right']:
        remove_width = int(w * percentage)
        if side == 'left':
            mask[ymin:ymax, xmin:xmin + remove_width] = 1
        elif side == 'right':
            mask[ymin:ymax, xmax - remove_width:xmax] = 1
    elif side == 'full':
        mask[ymin:ymax, xmin:xmax] = 1
    else:
        raise ValueError("Invalid side specified. Use 'top', 'bottom', 'left', 'right', or 'full'.")


    inpainted_image = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    #Save the inpainted image
    output_filename = os.path.join(output_folder, f'{image_id}.jpg')
    cv2.imwrite(output_filename, inpainted_image)
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
            break
        
        numbers = extract_number_from_sentence(sentence_path) #find the number for person tag
        bboxes = find_bounding_boxes(annotation_path, numbers) #find al the bounding boxes
        
        if not bboxes:
            print(f"No bounding boxes found for {image_id} with number {number}") #if there is not a person tag skip the image
            break
        
        max_bbox = max(bboxes, key=calculate_area) #calculate max bounding box
        #you can put the necessary work in here instead to the image with the bounding box
        # draw_bounding_box(image_path, bboxes, output_folder, image_id) 
        inpainted_image = inpaint_image(image_path, max_bbox, output_folder, image_id)


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
    #image_folder = 'flickr30k_images/test'
    #sentence_folder = os.path.join('flickr30k', 'Sentences')
    #annotation_folder = os.path.join('flickr30k', 'Annotations')
    #output_folder = 'output_images_noised'

    ###image_folder = './IMAGES_ATTACK/remove/10_images_original_8'
    ###sentence_folder = './IMAGES_ATTACK/remove/10_images_original_8/Sentences/'
    ###annotation_folder = './IMAGES_ATTACK/remove/10_images_original_8/Annotations/'
    ###output_folder = "./IMAGES_ATTACK/remove/10_images/left_50"
    image_folder = './DATASET_938_img/flickr30k/flickr30k_images/test/'
    sentence_folder = './DATASET_938_img/flickr30k/flickr30k/Sentences/'
    annotation_folder = './DATASET_938_img/flickr30k/flickr30k/Annotations/'
    output_folder = './DATASET_938_img/flickr30k/flickr30k_images/'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_images(image_folder, sentence_folder, annotation_folder, output_folder) #giving all the necessary folders
