# Labs 8: Ways to build an image data set.

This lab will cover some ways of buildig an image data set.  

## Attention
This lab requires a Flickr API key.  Please requrest a key at https://www.flickr.com/services/apps/create/apply/.

## Setup 
You'll be using a docker image for this lab and it is recommended that you run this on your workstation.

1. Create a data directory for the images.
2. Start the docker image
```docker run -ti -v <pathToYourDataDiretory>:/images/data ryandejana/lab8:v1 bash```

## Part 1: FFMPEG and Video
In the first part of this lab, you'll work with a video from https://www.jpjodoin.com/urbantracker/dataset.html and you'll be extracting images from it.

In the directory /images, you'll find the file sherbrooke_video.avi.  This is a 2 min and 13 second video filmed from a traffic camera located at at the Sherbrooke/Amherst intersection in Montreal.

You'll need to create the test directories ahead of time.  

```mkdir data/ffmepg```

```mkdir data/ffmepg/test1```

```mkdir data/ffmepg/test2```

```mkdir data/ffmepg/test3```

If you get errors in the following steps, you can extract to data/ and change the extracted image name pattern.

The first step is to extract a single image from the video.

```ffmpeg -i sherbrooke_video.avi -frames:v 1 data/ffmepg/test1/extracted.jpg```

the option ```-frames:v``` specifies the number of frames to extract and ```data/ffmepg/test1/extracted.jpg``` is the output file.  

When complete, browser your data directory from your workstation and open up ```data/ffmepg/test1/extracted.jpg``` and confirm that extract.

Now you wille extract 100 images from the file using the command 
```ffmpeg -i sherbrooke_video.avi -frames:v 100 data/ffmepg/test2/extract%04d.jpg```

With this command, ```%04d``` tells ffmpeg to name the extracted images with the serices with a 4 digit pattern, extract0001.jpg, extract0002.jpg, etc. Other numbers may be used, e.g. to use 2 numbers, the pattern would be ```%02d```.

Review the images.  How much did the scence change?

Now we'll adjust the frames per second used with the -r option, in this case with 1 frame per second.

```ffmpeg -i sherbrooke_video.avi -frames:v 100 -r 1 data/ffmepg/test2/extract%04d.jpg```

What's different?  What happens if you change r?

Finally, we'll extract all the images with the command
```ffmpeg -i sherbrooke_video.avi data/ffmepg/test3/extract%04d.jpg```

- How long did it take?  
- How many images did you get?  
- Which is the "best" approach?

## Part 2a: Downloading images from Google

This this part of the lab, you'll be using a tool called google-images-download (https://github.com/hardikvasa/google-images-download) to download images.  This tool allows you to search google and download images to your machine.  Note, the default installation is limited 100 miages per keyword.  See the github repository for details on how to download more and for the command line arguements.

Run a simple example that will search for Polar bears and Brown Bears. 

```googleimagesdownload --keywords "Polar bears, Brown bears" --limit 100 -o /images/data/google/test1 -f jpg```

- How long did it take to download the roughly 200 images (you may get some errors)?
- Review the images.  How accurate are they? 

Not all images on the web are licensed for you to reuse as you see fit.  This tool provides the ablity to search with different usage rights.  (see the repository for the options).  Run the command 
```googleimagesdownload --keywords "Polar bears, Brown bears" --limit 100 -o /images/data/google/test2 -f jpg
 -r labeled-for-nocommercial-reuse
```

Did you see any difference in your results?  

Experiment with your own search terms and with the different usage options. 
- What terms did you use?  
- How accurate where your results?  
- Did the usage options matter?

## Part 2b: Downloading images from Flickr

### Note, you must have a Flickr API key.

The tool datr (https://github.com/peerdavid/datr/) provides a simple python library and utitily.

The usage of datr.py is

```
Usage: datr.py [options]

Options:
  -h, --help            show this help message and exit
  -s SEARCH_TAGS, --search_tags=SEARCH_TAGS
                        A comma-delimited list of tags. Photos with one or
                        More of the tags listed will be returned. You can
                        exclude results that match a term by prepending it with
                        a - character.
  -t NUM_THREADS, --num_threads=NUM_THREADS
                        Number of downloader threads (speed up download)
  -p PATH, --path=PATH  Path where downloaded files should be saved
  -n MAX_NUM_IMG, --num_images=MAX_NUM_IMG
                        Max. number of images to download
  -l LICENSE, --license=LICENSE
                        License of images. 0=All Rights Reserved,
                        4=Attribution License, 6=Attribution-NoDerivs License,
                        3=Attribution-NonCommercial-NoDerivs License, 2
                        =Attribution-NonCommercial License, 1=Attribution-
                        NonCommercial-ShareAlike License, 5=Attribution-
                        ShareAlike License, 7=No known copyright restrictions,
                        8=United States Government Work, 9=Public Domain
                        Dedication (CC0) 10=Public Domain Mark
```
Edit the file /root/.datr and add your API Key and Secret.  Your file will need to look similar to:

```
[Settings]
API_KEY =  yourKey
API_SECRET = yourSecret
```

Change to the directory /images/datr and run the following command:

```python datr.py --num_images 100 --search_tags cat --license 9 --num_threads 20 --path /images/data/datr/test1```

- How long did it take to download the 100 images?  
- How accurate are the results?  
- Try searching Flickr's web UI with the same search term.  Are the results similar?

Now run the command with only 1 thread.

```python datr.py --num_images 100 --search_tags cat --license 9 --num_threads 1 --path /images/data/datr/test2```

- Did this take any longer? If so, how much?

This tool also supports the ability to select difference usage/license options.  

```python datr.py --num_images 100 --search_tags cat --license 0 --num_threads 20 --path /images/data/datr/test3```

- Did are the results any different?

Try with your own search terms and license options.  How were the results? 

Try running the same search terms with both google-images-download and datr.

- Which is giving better results for you?  How are they better?
- Which is faster?
- If you had to build your own image data set, which, if any would you use?  Why?


