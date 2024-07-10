# Checking the Robustness of a Visual Grounding model
## Introduction
Visual Grounding models are multimodal models which aim to aims to detect and locate objects in an image which are referred in a natural language expression. To ensure their reliability in real-world applications it's a crucial task to test their robustness.<br /><br />
This project aims to check robustness of the GLIP model for the task of Visual Grounding for predicting bounding boxes of persons.<br /><br />
It was developed as a students project in the course “Multimodal AI” at Technische Universität Darmstadt.
## Configuration
The required steps for evaluating or making predictions with the GLIP model are described in the [docker markdown file](docker/docker_workflow.md).
## Dataset
The flickr30k entities dataset was used in this project. A subset of test images can be found in the [dataset folder](10_DATASET).
## Robustness Check methods
For checking the robustness of the model three different methods were applied to parts of the person bounding box in each image. First parts of the person bounding box were removed. Second parts of the person bounding box were occluded by adding another object. Third noise was applied to parts of the person bounding box. The changed images can be found in the [images attack folder](IMAGES_ATTACK).
## Prediction and Evaluation
The images with the predicted bounding boxes can be found in the [predictions folder](PREDICTIONS_ATTACK) and the evaluation of the model by using the recall metrics can be found in the [evaluation folder](EVALUATION)
