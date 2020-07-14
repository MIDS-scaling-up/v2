FROM nvcr.io/nvidia/l4t-tensorflow:r32.4.3-tf2.2-py3

RUN apt-get update && apt-get install -y libfreetype6-dev

#
# JupyterLab
#
RUN pip3 install matplotlib
RUN pip3 install jupyter jupyterlab --verbose
#RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager@2

RUN jupyter lab --generate-config
RUN python3 -c "from notebook.auth.security import set_password; set_password('nvidia', '/root/.jupyter/jupyter_notebook_config.json')" 

RUN pip3 install PILLOW

COPY beginner.ipynb beginner.ipynb
COPY transfer_learning_with_hub.ipynb transfer_learning_with_hub.ipynb


CMD /bin/bash -c "jupyter lab --ip 0.0.0.0 --port 8888 --allow-root &> /var/log/jupyter.log" & \
	echo "allow 10 sec for JupyterLab to start @ http://localhost:8888 (password nvidia)" && \
	echo "JupterLab logging location:  /var/log/jupyter.log  (inside the container)" && \
	/bin/bash

