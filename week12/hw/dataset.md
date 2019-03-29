# Homework: Part 2 - Installing LazyNLP

## Overview

A straightfoward library that allows you to crawl, clean up, and deduplicate webpages to create massive monolingual datasets. Using this library, you should be able to create datasets larger than the one used by OpenAI for GPT-2.


1. SSH into your first node (gpfs1) and proceed to install the requisites for LazyNLP installation
```
  * sudo apt-get --purge remove gpfs.gss.pmcollector gpfs.gui
  * sudo apt-get install -y python3 python3-dev python3-  setuptools python3-pip
  * git clone https://github.com/chiphuyen/lazynlp.git
  * pip3 install -r requirements.txt
  * pip3 install .
 ``` 
2. Once the library is installed it could be used out of the Python bindings, more on that later.

3. Download the [The WikiText language modeling dataset](https://www.salesforce.com/products/einstein/ai-research/the-wikitext-dependency-language-modeling-dataset/)
  ```
  * wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip
  * apt install unzip
  * unzip wikitext-103-v1.zip
  * rm -rf wikitext-103-v1.zip
  ```
4. Let's use the library to crawl a medium size dataset, the approach we are going to use is getting dumps of URL's that have been deduplicated, we will just clean them and prepare for processing.
  ```
  * pip install gdown
  * gdown https://drive.google.com/uc?id=1hRtA3zZ0K5UHKOQ0_8d0BIc_1VyxgY51
  * unzip reddit_urls.zip
  ```
5. In step 4 a urls.txt file was downloaded, use it as a base with the contents of [crawler code](https://github.com/MIDS-scaling-up/v2/blob/master/week12/hw/crawler.py), main idea is to use the function lazynlp.download_pages()

6. Use the following URL dumps:
 ```
 * https://drive.google.com/file/d/1hRtA3zZ0K5UHKOQ0_8d0BIc_1VyxgY51/view
 * https://drive.google.com/file/d/1zIVaRaVqGP8VNBUT4eKAzW3gYWxNk728/view?usp=sharing
 * https://drive.google.com/file/d/1C5aSisXMC3S3OXBFbnETLeK3UTUXEXrC/view?usp=sharing
 * https://dumps.wikimedia.org/enwiktionary/20190301/enwiktionary-20190301-pages-articles-multistream.xml.bz2 (notice this is not a url.txt file but a text file)
  ```
7. Be creative with the crawler (multithread, run in background no up &) and put the data into the distributed storage, we will use for the class lab;

8. Feel free to suggest improvements and try to collect as much data as possible.


