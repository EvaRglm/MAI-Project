FROM pengchuanzhang/maskrcnn:ubuntu18-py3.7-cuda10.2-pytorch1.9
WORKDIR usr/local/bin
RUN pip install einops shapely timm yacs tensorboardX ftfy prettytable pymongo transformers inflect
VOLUME /teamspace/studios/this_studio/GLIP:/usr/local/bin
CMD python setup.py clean --all build develop --user