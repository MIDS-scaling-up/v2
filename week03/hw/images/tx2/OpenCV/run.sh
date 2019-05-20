docker run --rm --privileged --name opencv --device=/dev/video1:/dev/video1 -v "$PWD":/app -it opencv:dev python /app/proc_video.py
