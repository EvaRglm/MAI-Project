import os

def rename_files(directory):
    for filename in os.listdir(directory):
        number = filename.replace(".jpg", "")
        f = open("DATASET_s/flickr30k/flickr30k/test.txt", "a")
        f.write(number+"\n")
        f.close()

# Usage
directory_path = 'GLIP/output_images_noised_1000'
rename_files(directory_path)
