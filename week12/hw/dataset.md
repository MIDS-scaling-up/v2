# Homework: Part 2 - Installing LazyNLP

## Overview

A straightfoward library that allows you to crawl, clean up, and deduplicate webpages to create massive monolingual datasets. Using this library, you should be able to create datasets larger than the one used by OpenAI for GPT-2.


1. SSH into your first node (gpfs1) and proceed to install the requisites for LazyNLP installation
  * sudo apt-get --purge remove gpfs.gss.pmcollector gpfs.gui
  * sudo apt-get install -y python3 python3-dev python3-  setuptools python3-pip
  * git clone https://github.com/chiphuyen/lazynlp.git
  * pip3 install -r requirements.txt
  * pip3 install .
  
2. Once the library is installed it could be used out of the Python bindings, more on that later.

3. Download the [The WikiText language modeling dataset](https://www.salesforce.com/products/einstein/ai-research/the-wikitext-dependency-language-modeling-dataset/)
  * wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip
  * apt install unzip
  * unzip wikitext-103-v1.zip
  * rm -rf wikitext-103-v1.zip
  
4. Let's use the library to crawl a medium size dataset, the approach we are going to use is getting dumps of URL's that have been deduplicated, we will just clean them and prepare for processing.
  * pip install gdown
  * gdown https://drive.google.com/uc?id=1hRtA3zZ0K5UHKOQ0_8d0BIc_1VyxgY51
  * unzip reddit_urls.zip
  
5.   
  


