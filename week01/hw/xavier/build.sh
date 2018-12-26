#!/bin/sh

if [ ! -f cuda.tgz ]
then
	tar -C /usr/lib -zcvf cuda.tgz  aarch64-linux-gnu
	# /usr/lib/aarch64-linux-gnu
fi

docker build -t cudabase:dev -f Dockerfile.cudabase.dev .

# rm -f cuda.tgz
