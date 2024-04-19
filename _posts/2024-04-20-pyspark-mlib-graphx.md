# Exploring PySpark MLlib with the "mediumsearchdataset" from Kaggle
![](</assets/images/pyspark-mlib-sm.png>)

## Introduction
In this article, we'll explore the capabilities of PySpark MLlib using the "mediumsearchdataset" from Kaggle. We'll dive into various machine learning tasks, including natural language processing and graph analysis using GraphX. PySpark MLlib provides a powerful set of tools for handling large-scale datasets and building scalable machine learning models. So, let's get started!

## Dataset
The "mediumsearchdataset" is a dataset from Kaggle containing information about articles published on the Medium platform. It includes details such as the article title, author, publication, tags, and claps (a measure of appreciation). This dataset will be our companion as we explore PySpark MLlib.

## Prerequisites
To follow along with these examples, e.g., in a [jupyter](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html) notebook, you'll need to have at least 

## Loading the Dataset
First, let's load the "mediumsearchdataset" into a PySpark DataFrame using the `spark.read.csv()` function

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MediumSearchAnalysis").getOrCreate()

data = spark.read.csv("medium_search_dataset.csv", header=True, inferSchema=True)
```

With just a few lines of code, our dataset is ready for analysis.

## Text Processing with PySpark MLlib
Text preprocessing is a crucial step in natural language processing. PySpark MLlib offers various tools for tokenization, stop word removal, and feature extraction. Let's preprocess the article titles

```python
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer

tokenizer = Tokenizer(inputCol="title", outputCol="words")
data = tokenizer.transform(data)

stopwords_remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
data = stopwords_remover.transform(data)

cv = CountVectorizer(inputCol="filtered_words", outputCol="features")
cv_model = cv.fit(data)
data = cv_model.transform(data)
```

The article titles are now tokenized, cleaned of stop words, and converted into numerical feature vectors, ready for further analysis.

## Topic Modeling with LDA
Topic modeling helps discover latent topics in a collection of documents. PySpark MLlib provides the Latent Dirichlet Allocation (LDA) algorithm for this purpose. Let's apply LDA to the preprocessed article titles

```python
from pyspark.ml.clustering import LDA

lda = LDA(k=5, maxIter=10, featuresCol="features")
lda_model = lda.fit(data)

topics = lda_model.describeTopics(3)
topics.show(truncate=False)
```

The LDA model identifies 5 topics and retrieves the top 3 words for each topic, providing insights into the themes present in the articles.

## Graph Analysis with GraphX
PySpark MLlib integrates with GraphX, enabling graph processing capabilities. Let's construct a graph based on the article tags and perform some analysis

```python
from pyspark.sql.functions import collect_set, array_contains
from graphframes import GraphFrame

# Extract unique tags
tags_data = data.select("articleId", "tags").distinct()

# Create edges DataFrame
edges = tags_data.alias("a").join(tags_data.alias("b"), 
                                  array_contains("a.tags", "b.tags") & ("a.articleId" < "b.articleId"), 
                                  "inner") \
                 .select("a.articleId", "b.articleId")

# Create vertices DataFrame
vertices = data.select("articleId").distinct()

# Create GraphFrame
graph = GraphFrame(vertices, edges)

# Find connected components
cc = graph.connectedComponents()
cc.groupBy("component").count().orderBy("count", ascending=False).show()
```

We create a graph where articles are vertices, and edges exist between articles if they share common tags. Using the `connectedComponents()` method, we find connected components in the graph and display their sizes.

## Conclusion
PySpark MLlib is a comprehensive library for implementing machine learning workflows on large-scale datasets. In this article, we explored PySpark MLlib using the "mediumsearchdataset" from Kaggle, showcasing techniques for text processing, topic modeling with LDA, and graph analysis using GraphX.

PySpark MLlib offers a wide range of algorithms and utilities for various machine learning tasks, seamlessly integrating with the Spark ecosystem for distributed processing. By leveraging PySpark MLlib, you can build scalable and powerful machine learning models to extract insights from big data.

Remember to preprocess your data, experiment with different algorithms and parameters, and evaluate your models using relevant metrics. PySpark MLlib's documentation and community resources provide valuable guidance along the way.

With PySpark MLlib in your toolkit, you can tackle complex machine learning challenges and unlock the potential of large-scale datasets. Happy exploring and building amazing machine learning applications with PySpark MLlib!