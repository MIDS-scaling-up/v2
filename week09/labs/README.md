# Labs 9: Fun with OpenSeq2Seq

### Inference using a trained Machine Translation model

On your Jetson TX2, start an OpenSeq2Seq docker container in interactive mode:
```
# assuming your docker image is called "seq" - remember, you had to build it in the HW
# if you forgot to build it, use w251/openseq2seq:tx2-3.3_b39
# also, assuming your external hard drive is mounted in /data, pass it through using -v
docker run --privileged --name seq -v /data:/data -p 8888:8888 -ti seq bash
```

As of 3/5/2019, we still need to patch file open statements in  tokenizer_wrapper.py (sigh) like so:
```
# all occurrences, both 'r' and 'w', add encoding="utf-8", e.g.
with open(input_file1, 'r', encoding="utf-8")
```
While you are at it, similarly patch  /OpenSeq2Seq/open_seq2seq/utils/utils.py  (sigh)

If you like completeless, you can now download the entire en-de corpus.  Hint: it will take a while:
```
# assuming the corpus will go under /data/wmt16_de_en

scripts/get_en_de.sh /data/wmt16_de_en
```
Recall where you transferred your model that you trained in the cloud.  If you lost your model, just download one from [Nvidia](https://nvidia.github.io/OpenSeq2Seq/html/machine-translation.html), just pick the transformer-base.py version - we assume this is what you trained in the cloud.


Now, edit your local config file:
```
cd /OpenSeq2Seq
vi example_configs/text2text/en-de/transformer-base.py 
```
You will need to set the following:
```
# this is where your data is - if you downloaded all of it; or placed some of the files anyways
data_root="/data/wmt16_de_en/"
# this is where your trained model is
"logdir": "/data/models/Transformer-FP32-H-256",
```

Review the infer_params section at the end.  This is where we specify which files to use as input to our inference process.
