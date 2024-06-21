FROM pengchuanzhang/maskrcnn:ubuntu18-py3.7-cuda10.2-pytorch1.9
WORKDIR usr/local/bin
COPY ./GLIP .
RUN pip install torch==1.9.0 torchvision  torchaudio einops shapely timm yacs tensorboardX ftfy prettytable pymongo transformers inflect
CMD python setup.py build develop --user