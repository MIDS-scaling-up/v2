# docker run --runtime=nvidia --ipc=host --rm -v /data:/data -p 8899:8888 -d lab07


FROM nvcr.io/nvidia/pytorch:19.09-py3
# FROM nvcr.io/nvidia/pytorch:20.03-py3

RUN pip install albumentations
RUN pip install efficientnet_pytorch

COPY berkeley-mids-w251-week07-lab.ipynb /workspace
COPY w251-aptos-finetune.ipynb /workspace
COPY w251-aptos-pretrain.ipynb /workspace
COPY gray_all_b4_fixed_lr_1e-4_380.pt /workspace
COPY recursion_model.bin /workspace
EXPOSE 8888
CMD jupyter notebook  --no-browser --ip=0.0.0.0 --allow-root

