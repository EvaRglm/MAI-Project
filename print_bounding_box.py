import cv2
import pandas as pd

def draw_bounding_boxes(image, boxes, category_ids, scores, color=(0, 255, 0), thickness=2):
    for box, category_id, score in zip(boxes, category_ids, scores):
        x, y, w, h = box
        cv2.rectangle(image, (x, y), (x+w, y+h), color, thickness)
        label = f'Category: {category_id}, Score: {score:.2f}'
        cv2.putText(image, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)
    return image

def process_images(data_file):
    # Read the data file
    df = pd.read_csv(data_file)

    # Group the data by image_id
    grouped = df.groupby('image_id')

    for image_id, group in grouped:
        # Read the image
        image = cv2.imread(image_id)
        if image is None:
            print(f"Error: Image {image_id} not found.")
            continue

        # Extract bounding boxes, category_ids, and scores
        boxes = group[['x', 'y', 'width', 'height']].values
        category_ids = group['category_id'].values
        scores = group['score'].values

        # Draw bounding boxes on the image
        image_with_boxes = draw_bounding_boxes(image, boxes, category_ids, scores)

        # Save or display the image
        output_filename = f'output_{image_id}'
        cv2.imwrite(output_filename, image_with_boxes)
        print(f"Processed {image_id} and saved as {output_filename}")

if __name__ == "__main__":
    # Path to the data file
    data_file = 'data.csv'
    process_images(data_file)
