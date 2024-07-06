import os
import re
import cv2
import random
import xml.etree.ElementTree as ET


def extract_number_from_sentence(sentence_file):
    with open(sentence_file, 'r') as file:
        content = file.read()
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


def insert_image(image, insert_image_path, bbox):
    insert_img = cv2.imread(insert_image_path)
    if insert_img is None:
        print(f"Error: Image {insert_image_path} not found.")
        return

    xmin, ymin, xmax, ymax = bbox
    bbox_width = xmax - xmin
    bbox_height = ymax - ymin
    insert_width = bbox_width // 2  # Cover at most 1/2 of the bounding box width
    insert_height = bbox_height // 5  # Cover at most 1/5 of the bounding box height

    # Resize insert_img to fit the bounding box width and 1/5 height
    insert_img_resized = cv2.resize(insert_img, (insert_width, insert_height))

    # Insert the resized image into the topmost part of the bounding box
    insert_x_start = xmin + (bbox_width - insert_width) // 2
    image[ymin:ymin + insert_height, insert_x_start:insert_x_start + insert_width] = insert_img_resized


def draw_bounding_box(image_path, bboxes, output_folder, image_id, insert_image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Image {image_path} not found.")
        return

    max_bbox = max(bboxes, key=calculate_area)
    insert_image(image, insert_image_path, max_bbox)

    for bbox in bboxes:
        xmin, ymin, xmax, ymax = bbox
        color = (0, 255, 0)  # Green
        thickness = 2
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)

    output_filename = os.path.join(output_folder, f'output_{image_id}.jpg')
    cv2.imwrite(output_filename, image)
    print(f"Processed {image_id} and saved as {output_filename}")


def process_images(image_folder, sentence_folder, annotation_folder, output_folder, insert_images_folder):
    for image_filename in os.listdir(image_folder):  # open the image
        if not image_filename.endswith('.jpg'):
            continue

        image_id = os.path.splitext(image_filename)[0]  # take image name
        image_path = os.path.join(image_folder, image_filename)
        sentence_path = os.path.join(sentence_folder, image_id + '.txt')  # find the paths
        annotation_path = os.path.join(annotation_folder, image_id + '.xml')

        if not os.path.exists(sentence_path) or not os.path.exists(
                annotation_path):  # if there is a missing file skip this image
            print(f"Missing files for {image_id}")
            continue

        numbers = extract_number_from_sentence(sentence_path)  # find the number for person tag
        bboxes = find_bounding_boxes(annotation_path, numbers)  # find al the bounding boxes

        if not bboxes:
            print(
                f"No bounding boxes found for {image_id} with numbers {numbers}")  # if there is not a person tag skip the image
            continue

        insert_image_path = random.choice(
            [os.path.join(insert_images_folder, f) for f in os.listdir(insert_images_folder) if f.endswith('.jpg')])

        # Draw bounding boxes and insert random image
        draw_bounding_box(image_path, bboxes, output_folder, image_id, insert_image_path)


if __name__ == "__main__":
    image_folder = 'flickr30k_images'
    sentence_folder = os.path.join('flickr30k', 'Sentences')
    annotation_folder = os.path.join('flickr30k', 'Annotations')
    output_folder = 'output_images'
    insert_images_folder = 'object_images'  # Folder containing images to be inserted

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_images(image_folder, sentence_folder, annotation_folder, output_folder,
                   insert_images_folder)  # giving all the necessary folders
