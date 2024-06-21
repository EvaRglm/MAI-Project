# Create docker image
```bash
docker pull pengchuanzhang/maskrcnn:ubuntu18-py3.7-cuda10.2-pytorch1.9
docker run -it -v /teamspace/studios/this_studio:/usr/local/bin --gpus all 29e307b180e8 sh
# docker exec -it <container_name> sh
cd usr/local/bin
pip install torch==1.9.0 torchvision  torchaudio
pip install einops shapely timm yacs tensorboardX ftfy prettytable pymongo
pip install transformers
pip install inflect
python setup.py build develop --user
# git clone https://github.com/microsoft/GLIP.git
# cd GLIP
# mkdir PREDICTIONS
# mkdir MODEL
# cd MODEL
# git clone https://huggingface.co/harold/GLIP
# cd ..
python tools/test_grounding_net.py --config-file configs/pretrain/glip_Swin_T_O365_GoldG.yaml --weight MODEL/glip_tiny_model_o365_goldg.pth TEST.IMS_PER_BATCH 1 MODEL.DYHEAD.SCORE_AGG "MEAN" TEST.EVAL_TASK detection MODEL.DYHEAD.FUSE_CONFIG.MLM_LOSS False OUTPUT_DIR PREDICTIONS
```