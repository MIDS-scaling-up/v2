# [IS BEING REVISED] Apache Spark Introduction

There are numerous ways to run Apache Spark, even multiple cluster options. In this guide you'll use the simplest clustered configuration, Spark in a standalone cluster. Other options include Spark on a YARN cluster and Spark on a Mesos cluster. If you're interested in learning about these other clustered options, please ask about them in class.

## Provision machines

Provision three Centos 7 VSes in SoftLayer with 2 CPUs, 4GB RAM and a 100GB local hard drive. Name them spark1, spark2, and spark3.  We recommend that you select VMs without external network interfaces - to be absolutely safe - or if request normal VMs, shut external interfaces down.  This makes it very simple: when assembling the cluster, please use internal IP addresses.

## Configure connectivity between machines

Configure spark1 such that it can SSH to spark1, spark2, and spark3 without passwords using SSH keys, and by name. To do this, you'll need to configure /etc/hosts, generate SSH keys using ssh-keygen, and write the content of the public key to each box to the file /root/.ssh/authorized_keys (ssh-copy-id helps with key distribution).

## Install Java, SBT, and Spark on all nodes

Install packages:

```
curl https://bintray.com/sbt/rpm/rpm | sudo tee /etc/yum.repos.d/bintray-sbt-rpm.repo
yum install -y java-1.8.0-openjdk-devel sbt git
```
Set the proper location of JAVA_HOME and test it:

```
echo export JAVA_HOME=\"$(readlink -f $(which java) | grep -oP '.*(?=/bin)')\" >> /root/.bash_profile
source /root/.bash_profile
$JAVA_HOME/bin/java -version
```
Download and extract a recent, prebuilt version of Spark (link obtained from ):

```
curl https://d3kbcqa49mib13.cloudfront.net/spark-2.1.1-bin-hadoop2.7.tgz | tar -zx -C /usr/local --show-transformed --transform='s,/*[^/]*,spark,'
```
For convenience, set $SPARK_HOME:

```
echo export SPARK_HOME=\"/usr/local/spark\" >> /root/.bash_profile
source /root/.bash_profile
```


## Configure Spark

On __spark1__, create the new file `$SPARK_HOME/conf/slaves` and content:

    spark1
    spark2
    spark3

From here on out, all commands you execute should be done on __spark1__ only. You may log in to the other boxes to investigate job failures, but you can control the entire cluster from the master. If you plan to use the Spark UI, it's convenient to modify your workstation's `hosts` file so that Spark-generated URLs for investigating nodes resolve properly.  Also, review /etc/hosts on spark1 and see if you have the 127.0.0.1 spark1 line as the first one mentioning your node name.  If that is the case, comment it out and replace it with <ip_address spark1> where the ip address is the internal ip address of your node.  If you leave it as is, your slave nodes may not be able to connect to the master node when the cluster comes up.

## Start Spark from master

Configure Spark

On spark1, create the new file $SPARK_HOME/conf/slaves and content:

```
spark1
spark2
spark3
```
From here on out, all commands you execute should be done on spark1 only. You may log in to the other boxes to investigate job failures, but you can control the entire cluster from the master. If you plan to use the Spark UI, it's convenient to modify your workstation's hosts file so that Spark-generated URLs for investigating nodes resolve properly.

## Copy files to master

From spark1, clone the homework repo into /root.  Locate and note the directory containing the file moby10b.txt and the directory src; they should be in the directory /root/coursework/week10/hw/


## Start Spark from master

Once you’ve set up the conf/slaves file, you can launch or stop your cluster with the following shell scripts, based on Hadoop’s deploy scripts, and available in $SPARK_HOME/:

```
sbin/start-master.sh - Starts a master instance on the machine the script is executed on
sbin/start-slaves.sh - Starts a slave instance on each machine specified in the conf/slaves file
sbin/start-all.sh - Starts both a master and a number of slaves as described above
sbin/stop-master.sh - Stops the master that was started via the bin/start-master.sh script
sbin/stop-slaves.sh - Stops all slave instances on the machines specified in the conf/slaves file
sbin/stop-all.sh - Stops both the master and the slaves as described above
```
Start the master first, then open browser and see http://<master_ip>:8080/:

```
$SPARK_HOME/sbin/start-master.sh

starting org.apache.spark.deploy.master.Master, logging to /root/spark/sbin/../logs/spark-root-org.apache.spark.deploy.master.Master-1-spark1.out
```
Then, run the start-slaves script, refresh the window and see the new workers (note that you can execute this from the master).
```
$SPARK_HOME/sbin/start-slaves.sh

spark1: starting org.apache.spark.deploy.worker.Worker, logging to /usr/local/spark/sbin/../logs/spark-root-org.apache.spark.deploy.worker.Worker-1-spark1.out
spark3: starting org.apache.spark.deploy.worker.Worker, logging to /usr/local/spark/sbin/../logs/spark-root-org.apache.spark.deploy.worker.Worker-1-spark3.out
spark2: starting org.apache.spark.deploy.worker.Worker, logging to /usr/local/spark/sbin/../logs/spark-root-org.apache.spark.deploy.worker.Worker-1-spark2.out
```

### secure the VSI with Firewall
```
service firewalld start
firewall-cmd --permanent --zone=public --add-port=6066/tcp
firewall-cmd --permanent --zone=public --add-port=7077/tcp
firewall-cmd --permanent --zone=public --add-port=8080-8081/tcp
firewall-cmd --reload
```
## Assignment
### Calculating Pi

Run the command: $SPARK_HOME/bin/run-example SparkPi

*Question 1:* What value of PI to you get?  Why is the value not "exact"? For a hint, see $SPARK_HOME/examples/src/main/python/pi.py 

### Use the Spark shell
Start the spark-shell

    $SPARK_HOME/bin/spark-shell

At the shell prompt, `scala>`, execute:

    val textFile = sc.textFile("/usr/local/spark/README.md")

This reads the local text file "README.md" into a Resilient Distributed Dataset or RDD (cf. https://spark.apache.org/docs/latest/quick-start.html) and sets the immutable reference "textFile". You should see output like this:

    15/06/10 16:43:34 INFO SparkContext: Created broadcast 0 from textFile at <console>:21
    textFile: org.apache.spark.rdd.RDD[String] = README.md MapPartitionsRDD[1] at textFile at <console>:21

You can interact with an RDD object. Try calling the following methods from the Spark shell:

    textFile.count()

    textFile.first()

Finally, execute a Scala collection transformation method on the RDD and then interrogate the transformed RDD:

    val linesWithSpark = textFile.filter(line => line.contains("Spark"))

    linesWithSpark.count()

Exit the Spark shell with `CTRL-D`.

Using the spark-shell, read the local text file moby10b.txt (should be /root/coursework/week6/hw/apache_spark_introduction/moby10b.txt) into a Resilient Distributed Dataset

*Question 2:* How many lines does the file have?

*Question 3:* What is the first line?

*Question 4:* How many lines contain the text "whale"?

### Run SparkJava8Example

In this section, you will create a program and run it on spark1 in standalone mode.

Note, you'll need to delete or change your output directory after each run.

Locate the file src/spark/SparkJava8Example.java and open it in your favorite editor.

This file demonstrates a number of features of spark, including map, flatmap, filter, reduce, and dataframes.  Spend some time looking over this file before moving on.

From within the source directory, complile SparkJava8Example
```
    javac -cp .:$SPARK_HOME/jars/* spark/SparkJava8Example.java 
```

Now run the file using moby10b.txt as the input and an output directory of your choice.
```
    java -cp .:$SPARK_HOME/jars/* spark.SparkJava8Example /root/coursework/week10/moby10b.txt /<yourOutputDirectory>
```
*Question 5:* How many output files (ignore _SUCCESS file) does Spark write when the file RDD 
(file.saveAsTextFile( outputDirectory)) is written to the output directory?

*Question 5b:*  Change the line:
                              JavaRDD<String> file = sc.textFile(inputFile);
              to:
                              JavaRDD<String> file = sc.textFile(inputFile,1);
              and rerun the sample.  How many outfiles are created when the RDD is saved?  
              Explain the difference.
              
### Programing example

Assumptions: job is run against the cluster

In this part, you will submit a spark job to your cluster. Normally, you would have HDFS as the shared file system, but let's not worry about it for now.  Just copy moby10b.txt to the same location in each node.


To run a job against the cluster, you'll need to package your job as a jar file.  Using SparkJava8Example as an example, you may create a jar using the following:
```
   jar cvf job.jar spark/*.class
```

To submit a job to a spark cluster, you will need to use the $SPARK_HOME/bin/spark-submit command.  See https://spark.apache.org/docs/latest/submitting-applications.html for details.  For your SparkJava8Example example, the command would be:

```
$SPARK_HOME/bin/spark-submit --master spark://spark1:7077 --class spark.SparkJava8Example job.jar /root/coursework/week10/moby10b.txt /root/output
```


## Submission
Submit a document with your answers to the problems, the access information to your spark cluster, and the steps to run your job(s) for questions 1-5.
