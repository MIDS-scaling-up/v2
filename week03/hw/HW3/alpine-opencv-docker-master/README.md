# Pre-built OpenCV for Alpine Linux (armhf)

Building OpenCV, especially when building for a different architecture, is a very painful and long process. This repository contains a prebuilt version of OpenCV 3.3.0 that runs under Alpine Linux on the ARMv7 architecture (e.g. a Raspberry Pi 3). It also has a Dockerfile to get started quickly - or to build your own work on.

## Running manually

Note that OpenCV is compiled for Alpine 3.6, and against Python 3.6. Other versions will not work.

* Copy file `opencv-prebuilt/cv2.so` to `/usr/lib/python3.6/site-packages/cv2.so`
* Copy directory `opencv-prebuilt/include-opencv` to `/usr/local/include/opencv`
* Copy directory `opencv-prebuilt/include-opencv2` to `/usr/local/include/opencv2`
* Copy the content of `opencv-prebuilt/local-lib` into `/usr/local/lib`

After this you can install `numpy` and other libraries via `pip`.

## Running with Docker

1. Install Docker.
1. Build the container:

    ```
    $ docker build -t alpine-opencv-demo .
    ```

    **Note:** This still builds Pillow and numpy, which still takes a bit of time.

1. Open a shell into the container:

    ```
    $ docker run -i -t alpine-opencv-demo /bin/bash
    ```

1. Run the demo:

    ```
    $ cd home
    $ python corner-demo.py

    # inspect 'chessboard-corners.jpg' for the output image
    ```

## License and attribution

* `demo/corner-demo.py` from the [OpenCV documentation](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html), licensed under the 3-clause BSD License ([LICENSE](https://opencv.org/license.html)).
* `demo/chessboard.jpg` from [Staxringold via Wikipedia](https://en.wikipedia.org/wiki/Chessboard#/media/File:Chess_board_opening_staunton.jpg) - CC-BY-SA 3.0
* OpenCV is licensed under the 3-clause BSD License ([LICENSE](https://opencv.org/license.html)).
* Rest of the repository is Apache 2.0 licensed.
