# Homework: Part 2 LazyNLP

## Overview

[LazyNLP](https://github.com/chiphuyen/lazynlp) is a library / collection of scripts that allows you to crawl, clean up, and deduplicate webpages to create massive monolingual datasets. Using this library, you should be able to create datasets larger than the one used by OpenAI for GPT-2.


1. SSH into each node (gpfs1, gpfs2, gpfs3) and proceed to install the requisites for LazyNLP installation
```
  * yum install -y python3 python3-devel git
  * git clone https://github.com/chiphuyen/lazynlp.git
  * cd lazynlp
  * pip3 install -r requirements.txt
  * pip3 install .
 ``` 
2. Download the [The WikiText language modeling dataset](https://www.salesforce.com/products/einstein/ai-research/the-wikitext-dependency-language-modeling-dataset/) into the mounted distributed gpfs file system
  ```
  * cd /gpfs/gpfsfpo
  * wget https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip
  * apt install unzip
  * unzip wikitext-103-v1.zip
  * rm -rf wikitext-103-v1.zip
  ```
3. Let's use LazyNLP to crawl a small (Gutenberg AUS) and medium (Gutenberg US) datasets.  Once you download the lists of urls below, you will need to modify the [crawler](https://github.com/MIDS-scaling-up/v2/blob/master/week12/hw/crawler.py) to point at these URL files.  Process the AUS file first. How long did it take? Now, kick off processing on the US file -- obviously, it will take a while, and by now, you should have a reasonable idea how long.
 ```
 * # Gutenberg US. About 50K books, about 14GB of text.
 * gdown https://drive.google.com/uc?id=1zIVaRaVqGP8VNBUT4eKAzW3gYWxNk728
 * # AUS Gutenberg. About 4k books, 1GB of text.
 * https://drive.google.com/uc?id=1C5aSisXMC3S3OXBFbnETLeK3UTUXEXrC
 * https://dumps.wikimedia.org/enwiktionary/20190301/enwiktionary-20190301-pages-articles-multistream.xml.bz2 (notice this is not a url.txt file but a text file)
  ```
4. Now, let's process a larger deduplicated collection of Reddit URLs. There are 163 separate URL files here, containing altogether 23M URLs. Your task is to download them all. Hint: you have three nodes and you can run many crawlers in parallel.
  ```
  * # The reddit dataset
  * pip install gdown
  * gdown https://drive.google.com/uc?id=1hRtA3zZ0K5UHKOQ0_8d0BIc_1VyxgY51
  * unzip reddit_urls.zip
  ```
5. If you run into weird "out of space" errors when clearly there's space, check your inode count:
```
mmdf gpfsfpo -F
# if you see the below
[root@gpfs3 gpfsfpo]# mmdf gpfsfpo -F
Inode Information
-----------------
Number of used inodes:          206848
Number of free inodes:               0
Number of allocated inodes:     206848
Maximum number of inodes:       206848

# to fix:
mmchfs gpfsfpo --inode-limit 15M
Set maxInodes for inode space 0 to 15728640
Fileset root changed.
[root@gpfs3 gpfsfpo]# mmdf gpfsfpo -F
Inode Information
-----------------
Number of used inodes:          206848
Number of free inodes:           53248
Number of allocated inodes:     260096
Maximum number of inodes:     15728640
[root@gpfs3 gpfsfpo]
# all better!
```

5. Feel free to suggest improvements and go after other data sets as needed (e.g. if your class project requires them)

### To Turn In
1. How much disk space is used after step 4?
2. Did you parallelize the crawlers in step 4? If so, how? 
3. Describe the steps to de-duplicate the web pages you crawled.
4. Submit the list of files you that your LazyNLP spiders crawled (ls -la).


Credit / No-credit only.  

#Please do not destroy the GPFS cluster as we will use it in class for labs.  


