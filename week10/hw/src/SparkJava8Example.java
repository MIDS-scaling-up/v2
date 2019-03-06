package spark;

import java.util.Arrays;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import scala.Tuple2;

/*
 * 
 * This class is a collection of example designed to demonstrate Spark 2 and Java 8.
 * These examples will use the Java 8 lambda approach
 */


public class SparkJava8Example {


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
		if(args.length != 2){
			System.err.println("missing arguments: requires inputFile outputDirectory");
			System.exit(-1);
		}
		String inputFile = args[0];
		String outputDirectory = args[1];

		try(
				//these will auto close
				SparkSession spark = SparkSession.builder().config(sparkConf).getOrCreate();
				JavaSparkContext sc =   new JavaSparkContext(spark.sparkContext()); 
		){


			/*
			 Map and FlatMap Example
				from https://www.linkedin.com/pulse/difference-between-map-flatmap-transformations-spark-pyspark-pandey

				map :It returns a new RDD by applying a function to each element of the RDD.   Function in map can return only one item.

				flatMap: Similar to map, it returns a new RDD by applying  a function to each element of the RDD, but output is flattened.
				Also, function in flatMap can return a list of elements (0 or more)

			 */
			List<Integer> data = Arrays.asList(3,4,5);
			JavaRDD<Integer> distData = sc.parallelize(data);
			//this is the map function
			List<List<Integer>> mapInts =  distData.map(x -> IntStream.range(1, x).boxed().collect(Collectors.toList())).collect();
			//output from map is [[1,2],[1,2,3],[1,2,3,4]], a list of lists
			System.out.println(mapInts);
			//this is the flatmap function
			List<Integer> intList = distData.flatMap(x ->  IntStream.range(1, x).boxed().collect(Collectors.toList()).iterator()).collect();
			/*
			//this is the "legacy" approach, creating an inner class.
			List<Integer> intList = distData.flatMap(new FlatMapFunction<Integer, Integer>() {

				@Override
				public Iterator<Integer> call(Integer x) throws Exception {
					//IntStream.range(1, x).toArray();
					List<Integer> intList =  IntStream.range(1, x).boxed().collect(Collectors.toList());


					return intList.iterator();
				}

			}).collect();
			 */
			//mapInts = distData.flatMap( x -> Arrays.asList(IntStream.range(1, x).toArray()).iterator()).collect();
			//output from map [1, 2, 1, 2, 3, 1, 2, 3, 4], a single list
			System.out.println(intList);
			//Read the file in using the default partitioning
			JavaRDD<String> file = sc.textFile(inputFile);
			//take (get) the first 10 lines of the file and display them
			System.out.println("");
			System.out.println("Orginal file: " + file.take(10));
			//write the original file out
			//pay attention to what spark writes out
			file.saveAsTextFile( outputDirectory);
			
			//let's change the file to be all CAPS
			//Now map the files contents to all upper case.
			JavaRDD<String> upperCaseFile = file.map(line -> line.toUpperCase());
			//display the first 10
			System.out.println("");
			System.out.println("Upper case: " + upperCaseFile.take(10));

			//now remove the lines not containing the word Moby
			JavaRDD<String> mobyFile =  file.filter(line -> line.contains("Moby"));
			System.out.println("");
			System.out.println("Moby: " + mobyFile.take(10));
			//finally, get an RDD of all the words
			JavaRDD<String> words = file.flatMap(line -> Arrays.asList(line.split(" ")).iterator());
			System.out.println("");
			System.out.println("Words: " + words.take(10));

			//Map Reduce example: count number of time each word appears
			//this maps each word to a tuple, (word,1) then reduces by key, summing up all occurrences of each word
			JavaPairRDD<String, Integer> counts =  words.mapToPair(word -> new Tuple2<>(word,1)).reduceByKey((x,y) -> x+y);
			//now sort by the key - this will be expensive with large data sets
			JavaPairRDD<String, Integer> sorted = counts.sortByKey();
			//take (get) the first 10
			System.out.println("");
			System.out.println("Word count: " + sorted.take(10));

			//dataframe example - see https://spark.apache.org/docs/latest/sql-programming-guide.html for details
			Dataset<Row> df = spark.read().text(inputFile);
			//get the first 10 items as a java list
			System.out.println(df.takeAsList(10));
			//this prints the schema of the dataframe
			df.printSchema();
			//simple query
			df.select("value").show();
			//sql query - creating a "table" called lines
			df.createOrReplaceTempView("lines");
			//this is an SQL query from the table "lines"
			spark.sql("select * from lines").show();
		}
	}
}
