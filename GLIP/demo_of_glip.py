# -*- coding: utf-8 -*-
"""Demo of GLIP

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12x7v-_miN7-SRiziK3Cx4ffJzstBJNqb

# GLIP

Welcome to the demo notebook for GLIP https://github.com/microsoft/GLIP!
"""

# Install CUDA 10.2; newer versions of CUDA may fail
# !apt-get update -y
# !apt-get --purge remove "*cublas*" "cuda*" "nsight*"
# !nvcc --version

# !wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
# !mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
# !wget https://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda-repo-ubuntu1804-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb
# !dpkg -i cuda-repo-ubuntu1804-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb
# !apt-key add /var/cuda-repo-10-2-local-10.2.89-440.33.01/7fa2af80.pub
# !apt-get update
# !apt-get -y install cuda

# Commented out IPython magic to ensure Python compatibility.
# Install Environments. This will take a few minutes. Please be patient ;)
# ! nvidia-smi
# ! git clone https://github.com/microsoft/GLIP.git
# # % cd GLIP
# ! git checkout c663d9db8a503e04c6b76cd2e14152bab775d28a
# ! pip install torch==1.9.0 torchvision  torchaudio
# ! pip install einops shapely timm yacs tensorboardX ftfy prettytable pymongo
# ! pip install transformers
# ! python setup.py build develop --user
# ! mkdir MODEL

import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

import json
import requests
from io import BytesIO
from PIL import Image
import numpy as np
pylab.rcParams['figure.figsize'] = 20, 12
from maskrcnn_benchmark.config import cfg
from maskrcnn_benchmark.engine.predictor_glip import GLIPDemo

def load(image_path):
    """
    Given an url of an image, downloads the image and
    returns a PIL image
    """
    # response = requests.get(url)
    pil_image = Image.open(image_path).convert("RGB")
    # convert to BGR format
    image = np.array(pil_image)[:, :, [2, 1, 0]]
    return image

def imshow(img, caption, output_file_path):
    plt.clf()
    plt.imshow(img[:, :, [2, 1, 0]])
    plt.axis("off")
    plt.figtext(0.5, 0.09, caption, wrap=True, horizontalalignment='center', fontsize=20)
    plt.savefig(output_file_path + '.jpg')

# Use this command for evaluate the GLPT-T model
# ! wget https://penzhanwu2bbs.blob.core.windows.net/data/GLIPv1_Open/models/glip_tiny_model_o365_goldg_cc_sbu.pth -O MODEL/glip_tiny_model_o365_goldg_cc_sbu.pth
config_file = "configs/pretrain/glip_Swin_T_O365_GoldG.yaml"
weight_file = "MODEL/glip_tiny_model_o365_goldg.pth"

# Use this command to evaluate the GLPT-L model
# ! wget https://penzhanwu2bbs.blob.core.windows.net/data/GLIPv1_Open/models/glip_large_model.pth -O MODEL/glip_large_model.pth
# config_file = "configs/pretrain/glip_Swin_L.yaml"
# weight_file = "MODEL/glip_large_model.pth"

# update the config options with the config file
# manual override some options
cfg.local_rank = 0
cfg.num_gpus = 1
cfg.merge_from_file(config_file)
cfg.merge_from_list(["MODEL.WEIGHT", weight_file])
cfg.merge_from_list(["MODEL.DEVICE", "cuda"])

glip_demo = GLIPDemo(
    cfg,
    min_image_size=800,
    confidence_threshold=0.7,
    show_mask_heatmaps=False
)

"""Next, we retrieve an image on which we wish to test the model. Here, we use an image from the validation set of COCO"""

# Predict test images
# v = 'test' or 'val'
image_file_path = 'DATASET/flickr30k/flickr30k_images/test/'
annotation_file_path = 'DATASET/mdetr_annotations/final_flickr_separateGT_test.json'
output_file_path = 'PREDICTIONS/'
def f(image_file_path, annotation_file_path, output_file_path):
    with open(annotation_file_path, 'r') as file:
        json_data = json.load(file)
    file_names = []
    for image_annotation in json_data.get('images', []):
        file_name = image_annotation.get('file_name')
        if file_name not in file_names:
            file_names.append(file_name)
            image = load(image_file_path + file_name)
            caption = image_annotation.get('caption')
            file_name = file_name.replace(".jpg", "")
            result, _ = glip_demo.run_on_web_image(original_image=image, original_caption=caption, thresh=0.6, output_file_path=output_file_path+file_name)
            imshow(result, caption, output_file_path + file_name)
f(image_file_path, annotation_file_path, output_file_path)

# output_file_path = 'output_images_noised_10/PREDICTIONS/output_7998492801'
# image = load('output_images_noised_10/output_7998492801.jpg')
# caption = 'On a football field, a football player wearing a Raiders uniform carries a football and runs away from a football player wearing a Dolphins uniform.'
# result, _ = glip_demo.run_on_web_image(original_image=image, original_caption=caption, thresh=0.6, output_file_path=output_file_path)
# imshow(result, caption, output_file_path)

# image = load('http://farm4.staticflickr.com/3693/9472793441_b7822c00de_z.jpg')
# caption = 'sofa . remote . dog . person . car . sky . plane .' # the caption can also be the simple concatonation of some random categories.
# result, _ = glip_demo.run_on_web_image(image, caption, 0.5)
# imshow(result, caption)