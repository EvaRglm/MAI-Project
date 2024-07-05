## Evaluation
- Recall: TP/TP+FN
- For each image_sentence prediction and for each phrase of that iou values between all bounding boxes of each phrase are calculated. After that it is tested whether the max iou value within a certain range ([:1],[:5],[:10],[:]) exceeds the iou threshold.
    - if exceeding --> add 1 to TP and FN
    - else --> add 1 to FN
- After iterating over all Predictions, the Recall values are calculated.