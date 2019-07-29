# Labs 9: Fun with OpenSeq2Seq

### Inference using a trained Machine Translation model

On your Jetson TX2, start an OpenSeq2Seq docker container in interactive mode:
```
# assuming your docker image is called "seq" - remember, you had to build it in the HW
# if you forgot to build it, use w251/openseq2seq:dev-tx2-4.2_b158-py3
# also, assuming your external hard drive is mounted in /data, pass it through using -v
docker run --privileged --name seq -v /data:/data -p 8888:8888 -ti seq bash
```

As of 7/2/2019, we still need to patch file open statements in  tokenizer_wrapper.py (sigh) like so:
```
# all occurrences, both 'r' and 'w', add encoding="utf-8", e.g.
with open(input_file1, 'r', encoding="utf-8")
```
While you are at it, similarly patch (sigh):
```
# there is just one occurrence of open() here:
/OpenSeq2Seq/open_seq2seq/data/text2text/text2text.py

/OpenSeq2Seq/open_seq2seq/utils/utils.py:
# in def deco_print()
# replace in  else:
# print((start + " " * offset + line).encode('utf-8'), end=end)
```

If you like completeless, you can now download the entire en-de corpus.  Hint: it will take a while:
```
# assuming the corpus will go under /data/wmt16_de_en

scripts/get_en_de.sh /data/wmt16_de_en
```
A more practical way would be to copy the three files that we included in this directory: [m_common.vocab](m_common.vocab), [m_common.model](m_common.model),  [wmt14-en-de.src.BPE_common.32K.tok](wmt14-en-de.src.BPE_common.32K.tok), and [wmt14.tiny.tok](wmt14.tiny.tok) and place them into your data directory -- we'll assume it is /data/wmt16_de_en for now.

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

# we don't have Horovod installed on our Jetson!
"use_horovod": False,
```

Review the infer_params section at the end.  This is where we specify which files to use as input to our inference process.  Note that the default inference file is wmt14-en-de.src.BPE_common.32K.tok .  That is fine and should give you some reasonable idea about the bleu score of your model, but inference will take a while.  We suggest replacing it with wmt14.tiny.tok, which is only 10 lines long.  

Now, we should be able to run the inference!
```
cd /OpenSeq2Seq
python3 run.py --config_file=example_configs/text2text/en-de/transformer-base.py --mode=infer --infer_output_file=raw.txt --num_gpus=1
```
Note the output of the inference is tokenized, so we must detokenize it:
```
python3 tokenizer_wrapper.py --mode=detokenize --model_prefix=/data/wmt16_de_en/m_common --decoded_output=result.txt --text_input=raw.txt
```
The result of your hard work should now be in ```result.txt``` !

### Troubleshooting
* If you get a massive error with a lot of output eventually pointin to out of memory errors during the loading of your model snapshot, just reboot your jetson at try again.
* Similarly, if you encounter errors during inference, make sure that you do specify a target_file in the infer_params section of your configuration file.  See below my configuration. The a.txt file here must exist and have the same number of lines or longer than the source_file.  This is a bug in OpenSeq2Seq. Here, I just edited a.txt and added 11 files to it (my source_file has 10 lines).
```
    "source_file": "/data/wmt16_de_en/questions_en.tok.txt",
    "target_file": "/data/wmt16_de_en/a.txt",

```
### Notes
* This language to language translation model is generic: it does not care which languages are used, or whether in fact these are languages at all.  It just learns to convert between pairs of strings.  It could be used to train a simple chatbot, for instance
* You can add any other language to the model, just add the data prep instructions and issue a pull request into OpenSeq2Seq
* Inference time is about 4-5 seconds (batch size 1)  on a TX2

