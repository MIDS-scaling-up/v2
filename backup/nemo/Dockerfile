FROM w251/pytorch:dev-tx2-4.3_b132

# This container is called w251/nemo:dev-tx2-4.3_b132
# You will need to pull the data first and place it into /data like we did:
# docker run --privileged -v /data:/data nemo python3 scripts/get_librispeech_data.py --data_root=/data/librispeech --data_set=dev_clean
# You wil need to download the pre-trained weights from here: https://ngc.nvidia.com/catalog/models/nvidia:quartznet15x5 and place them, like we did, under /data/models/QuartzNet15x5

# Now you can try doing the inference.
# docker run --privileged -v /data:/data nemo python3 examples/asr/jasper_eval.py --model_config=examples/asr/configs/quartznet15x5.yaml --eval_datasets "/data/librispeech/dev_clean.json" --load_dir=/data/models/QuartzNet15x5/


WORKDIR /tmp
RUN git clone https://github.com/NVIDIA/apex
WORKDIR /tmp/apex
RUN pip3 install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./

WORKDIR /tmp

# RUN pip install --upgrade pip

RUN apt update
RUN apt install -y cmake
RUN git clone https://github.com/NVIDIA/NeMo.git
WORKDIR /tmp/NeMo

RUN apt install -y protobuf-compiler libprotobuf-dev
# RUN ./reinstall.sh
RUN pip3 install nemo-toolkit  # installs NeMo Core

RUN apt install -y libatlas-base-dev libblas-dev liblapack-dev gfortran
# RUN pip3 install "scipy>=1.0.0"
RUN pip3 install "scipy==1.3.3"
RUN apt install -y libffi-dev
RUN pip3 install cython
RUN pip3 install scikit-learn
RUN pip3 install cffi
RUN apt install -y llvm-7-dev llvm-7 llvm-7-runtime
ENV LLVM_CONFIG /usr/lib/llvm-7/bin/llvm-config
# RUN find / -name llvm-config
RUN pip3 install llvmlite
RUN pip3 install nemo-asr # installs NeMo ASR collection
# RUN pip3 install nemo-nlp # installs NeMo NLP collection
RUN apt install -y python3-matplotlib
RUN pip3 install nemo-tts # installs NeMo TTS collection
# RUN rm -fr /tmp/apex /tmp/NeMo

WORKDIR /tmp
RUN git clone https://github.com/google/sentencepiece.git
RUN mkdir /tmp/sentencepiece/build
WORKDIR  /tmp/sentencepiece/build
RUN cmake ..
RUN make -j 6
RUN make install
RUN ldconfig -v 
WORKDIR /tmp/sentencepiece/python
RUN python3 setup.py build
RUN python3 setup.py install
# RUN pip3 install sentencepiece
RUN apt install -y libhdf5-dev
RUN pip3 install nemo-nlp

RUN pip3 install wrapt
RUN pip3 uninstall -y pillow
RUN pip3 install 'pillow<7'
RUN apt install -y libsndfile1
RUN pip3 install frozendict

# RUN pip3 install nemo-nlp
WORKDIR /tmp/NeMo
# comment out the requirement for onnxruntime
RUN sed -i "s/onnxruntime/#onnxruntime/g" requirements/requirements.txt 

# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -O
RUN curl -f -L https://static.rust-lang.org/rustup.sh -O
RUN sh rustup.sh -y
ENV PATH /root/.cargo/bin:$PATH 
RUN echo $PATH
RUN rustc --version
RUN ./reinstall.sh
# RUN python3 -m unittest tests/*.py
# WORKDIR /
