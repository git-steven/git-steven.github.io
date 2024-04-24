from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark import SparkFiles
from graphframes import GraphFrame

# spark = SparkSession.builder.master("spark://localhost:7077").appName("HarryPotterAnalysis").getOrCreate()

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

spark.catalog.clearCache()

spark.catalog.clearCache()
character_path = SparkFiles.get("hp_characters.csv")
print(character_path)


character_df = spark.read.csv(character_path, header=True, inferSchema=True)

# Extract unique characters
characters = character_df.select("Name").distinct()
loyalty = character_df.select("Loyalty").distinct()

# Create edges DataFrame
edges = character_df.select("Id", "name", "loyalty") \
    .withColumnRenamed("Id", "id") \
    .withColumnRenamed("Name", "src") \
    .withColumnRenamed("loyalty", "dst") \

display_df(edges,5)

# Create vertices DataFrame
vertices = characters.withColumnRenamed("Name", "id")

# Create GraphFrame
graph = GraphFrame(vertices, edges)

# Find connected components
cc = graph.connectedComponents()
cc.groupBy("component").count().orderBy("count", ascending=False).show()