### Using Spark with Intel BigDL
This lab assumes that you have three CentOS or RedHat servers available (names spark1, spark2, and spark3). We recommend using the VMs from your homework.


In this lab, we are experimenting with [Intel's BigDL](https://github.com/intel-analytics/BigDL), a distributed Deep Learning framework developed specifically for Intel hardware

We will use the code from the link below with some minor modification.  Feel free to go over it time permitting:
https://bigdl-project.github.io/0.2.0/#PythonUserGuide/python-examples/

### Installing BigDL
Download and install BigDL on the master node
```
# on the master node only
cd /usr/local
mkdir -m 777 bigdl
cd bigdl
wget https://oss.sonatype.org/content/groups/public/com/intel/analytics/bigdl/dist-spark-2.1.1-scala-2.11.8-linux64/0.3.0/dist-spark-2.1.1-scala-2.11.8-linux64-0.3.0-dist.zip
unzip *.zip
rm *.zip
```
Make sure rsync is installed everywhere
```
yum install rsync
ssh spark2 yum install rsync
ssh spark3 yum install rsync
```
Now, propagate BigDL directory to other nodes
```
# repeat for all slave nodes
cd /usr/local
rsync -avz bigdl spark2:/usr/local
rsync -avz bigdl spark3:/usr/local
```
Make sure you have numpy installed:
```
yum install -y numpy
```

### Validating the install
To get a python shell with BigDL you do this:
```
cd /usr/local/bigdl/lib
export BIGDL_HOME=/usr/local/bigdl
cd $BIGDL_HOME/lib
BIGDL_VERSION=0.3.0
${SPARK_HOME}/bin/pyspark --master local[2] \
--conf spark.driver.extraClassPath=bigdl-SPARK_2.1-${BIGDL_VERSION}-jar-with-dependencies.jar \
--py-files bigdl-${BIGDL_VERSION}-python-api.zip \
--properties-file ../conf/spark-bigdl.conf
```
Assuming it started with no errors, see if you can create a basic linear layer:
```
from bigdl.util.common import *
from pyspark import SparkContext
from bigdl.nn.layer import *
import bigdl.version

# create sparkcontext with bigdl configuration
sc = SparkContext.getOrCreate(conf=create_spark_conf()) 
init_engine() # prepare the bigdl environment 
bigdl.version.__version__ # Get the current BigDL version
linear = Linear(2, 3) # Try to create a Linear layer
```
### Training LeNet
LeNet is a classic neural network developed in the late 90's to classify handwritten digits
Let us pick a directory and clone Intel's BigDL examples directory
```
cd /root
git clone https://github.com/intel-analytics/BigDL
cd BigDL
git checkout branch-0.3
```

We will need to install a package called six:
```
pip install six
ssh spark2 pip install six
ssh spark3 pip install six
```

Now, create a script file called lenet.sh and write the following into it:
```
#!/bin/sh

PYTHONHASHSEED=0
BIGDL_VERSION=0.3.0
BigDL_HOME=/usr/local/bigdl
GITHUB_BIGDL_HOME=/root/BigDL
SPARK_HOME=/usr/local/spark
MASTER=local[2]

PYTHON_API_ZIP_PATH=${BigDL_HOME}/lib/bigdl-0.3.0-python-api.zip
BigDL_JAR_PATH=${BigDL_HOME}/lib/bigdl-SPARK_2.1-0.3.0-jar-with-dependencies.jar

# BigDL_JAR_PATH=${BigDL_HOME}/dist/lib/bigdl-VERSION-jar-with-dependencies.jar
PYTHONPATH=${PYTHON_API_ZIP_PATH}:$PYTHONPATH

        ${SPARK_HOME}/bin/spark-submit \
            --master ${MASTER} \
            --driver-cores  2 \
            --driver-memory 2g  \
            --total-executor-cores  2 \
            --executor-cores 4  \
            --executor-memory 4g \
            --py-files ${PYTHON_API_ZIP_PATH},${GITHUB_BIGDL_HOME}/pyspark/bigdl/models/textclassifier/textclassifier.py  \
            --jars ${BigDL_JAR_PATH} \
            --conf spark.driver.extraClassPath=${BigDL_JAR_PATH} \
            --conf spark.executor.extraClassPath=bigdl-SPARK_1.6-0.3.0-SNAPSHOT-jar-with-dependencies.jar \
            --conf spark.executorEnv.PYTHONHASHSEED=${PYTHONHASHSEED} \
            ${GITHUB_BIGDL_HOME}/pyspark/bigdl/models/textclassifier/textclassifier.py \
             --max_epoch 3 \
             --model cnn
```
Let us run it:
```
chmod a+x lenet.sh
./lenet.sh
```
IF all goes well, you should see something like:
```
2017-10-16 18:41:14 INFO  DistriOptimizer$:374 - [Epoch 3 16000/15958][Iteration 375][Wall Clock 58.496114957s] Epoch finished. Wall clock time is 59357.355329 ms
2017-10-16 18:41:14 INFO  DistriOptimizer$:626 - [Wall Clock 59.357355329s] Validate model...
2017-10-16 18:41:15 INFO  DistriOptimizer$:668 - Top1Accuracy is Accuracy(correct: 3878, count: 4039, accuracy: 0.9601386481802426
```
