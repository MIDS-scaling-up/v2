package spark;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.SparkSession;

/*
Compile steps.
1. Define SPARK_HOME
2. javac -cp .:$SPARK_HOME/jars/* spark/JavaSparkTemplate.java 

Execution steps
1. Define SPARK_HOME
2. java -cp .:$SPARK_HOME/jars/* spark.JavaSparkTemplate

*/

public class JavaSparkTemplate {

	
	public static void main(String[] args) {
		//this controls a lot of spark related logging
		//comment or change logging level as needed
		Logger.getLogger("org").setLevel(Level.OFF);
		Logger.getLogger("akka").setLevel(Level.OFF);
		
		
		
		SparkConf sparkConf = new SparkConf().setAppName("HW6");
		if (!sparkConf.contains("spark.master")) {
			//this sets the job to use 2 executors locally
		    sparkConf.setMaster("local[2]");
		}
		
		
		try(
			//these will auto close
			SparkSession spark = SparkSession.builder().config(sparkConf).getOrCreate();
			JavaSparkContext sc =   new JavaSparkContext(spark.sparkContext()); 
		){
			//Spark stuff here...
		}
	}
}
