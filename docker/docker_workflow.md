# Create docker image
```bash
docker pull pengchuanzhang/maskrcnn:ubuntu18-py3.7-cuda10.2-pytorch1.9
docker run -it -v /teamspace/studios/this_studio/GLIP:/usr/local/bin --ipc=host --gpus all 29e307b180e8 sh
cd usr/local/bin
pip install einops shapely timm yacs tensorboardX ftfy prettytable pymongo transformers inflect
python setup.py build develop --user
# # Flickr 30k Evaluation
# python tools/test_grounding_net.py --config-file configs/pretrain/glip_Swin_T_O365_GoldG.yaml --task_config configs/flickr/test.yaml,configs/flickr/val.yaml --weight MODEL/glip_tiny_model_o365_goldg.pth OUTPUT_DIR PREDICTIONS TEST.IMS_PER_BATCH 1 SOLVER.IMS_PER_BATCH 1 TEST.MDETR_STYLE_AGGREGATE_CLASS_NUM 100 TEST.EVAL_TASK grounding MODEL.DYHEAD.FUSE_CONFIG.MLM_LOSS False
# Flickr 30k Prediction
python demo_of_glip.py
```