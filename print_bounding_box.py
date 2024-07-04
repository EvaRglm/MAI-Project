import cv2
import json

def draw_bounding_boxes(image, boxes, scores, color=(0, 255, 0), thickness=2):
    for box, score in zip(boxes, scores):
        x, y, w, h = map(int, box)
        cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
        label = f'Score: {score:.2f}'
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)
    return image

def process_images(data_file):
    # Load the JSON data
    with open(data_file, 'r') as file:
        data = json.load(file)

    # Process each image's data
    for item in data:
        image_id = item['image_id']
        boxes = item['boxes'][0]  # Extracting the first list of boxes for simplicity
        scores = item['scores'][0]  # Extracting the first list of scores for simplicity

        # Construct the image file name
        image_filename = f'{image_id}.jpg'
        
        # Read the image
        image = cv2.imread(image_filename)
        if image is None:
            print(f"Error: Image {image_filename} not found.")
            continue

        # Draw bounding boxes on the image
        image_with_boxes = draw_bounding_boxes(image, boxes, scores)

        # Save or display the image
        output_filename = f'output_{image_id}.jpg'
        cv2.imwrite(output_filename, image_with_boxes)
        print(f"Processed {image_filename} and saved as {output_filename}")

if __name__ == "__main__":
    # Path to the data file
    data_file = '/mnt/data/bbox.json'
    process_images(data_file)
