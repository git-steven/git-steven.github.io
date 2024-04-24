# Exploring the Seven Kingdoms of PySpark MLlib with Game of Thrones Dialogue

Hello, dear readers! Today, we embark on a thrilling adventure through the realm of PySpark MLlib, armed with the sacred texts of the "Game of Thrones" series scripts. In this somewhat lighthearted exploration, we shall uncover the hidden secrets within these ancient scrolls using the mystical powers of machine learning. So, grab your dragonglass and let's dive in!


First, let us load the [Game of Thrones scripts](https://www.kaggle.com/datasets/anderfj/game-of-thrones-series-scripts-breakdowns) from the distant land of Kaggle, where the "anderfj/game-of-thrones-series-scripts-breakdowns" dataset resides. With a few lines of incantation, we shall load these precious scripts into a PySpark DataFrame:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("GameOfThronesAnalysis").getOrCreate()

data = spark.read.csv("got_scripts_breakdown.csv", header=True, inferSchema=True)
```

Behold! The dialogue is now at our command, ready to be analyzed by the all-seeing eye of PySpark MLlib.

Next, let us cast a spell of text preprocessing upon the scripts. We shall tokenize the words, banish the stop words, and transform the scripts into a numerical representation fit for machine learning:

```python
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer

tokenizer = Tokenizer(inputCol="script", outputCol="words")
data = tokenizer.transform(data)

stopwords_remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
data = stopwords_remover.transform(data)

cv = CountVectorizer(inputCol="filtered_words", outputCol="features")
cv_model = cv.fit(data)
data = cv_model.transform(data)
```

Lo and behold! The scripts have been transformed, ready to reveal their innermost secrets.

Now, let us summon the power of Latent Dirichlet Allocation (LDA) to uncover the hidden topics within the scripts. With LDA as our guide, we shall peer into the very essence of the Seven Kingdoms:

```python
from pyspark.ml.clustering import LDA

lda = LDA(k=7, maxIter=10, featuresCol="features")
lda_model = lda.fit(data)

topics = lda_model.describeTopics(3)
topics.show(truncate=False)
```

Behold, the Seven Kingdoms of topics have been revealed! Each topic represents a fundamental aspect of the Game of Thrones universe, from the intricate web of character relationships to the epic battles that shape the fate of Westeros.

But wait, there's more! Let us delve deeper into the connections between the characters using the arcane art of GraphX. We shall create a graph where characters are nodes, and edges represent their interactions within the scripts:

```python
from pyspark.sql.functions import collect_set, array_contains
from graphframes import GraphFrame

# Extract unique characters
characters_data = data.select("character").distinct()

# Create edges DataFrame
edges = data.alias("a").join(data.alias("b"), 
                             array_contains("a.script", "b.script") & ("a.character" < "b.character"), 
                             "inner") \
            .select("a.character", "b.character")

# Create vertices DataFrame
vertices = characters_data.withColumnRenamed("character", "id")

# Create GraphFrame
graph = GraphFrame(vertices, edges)

# Find connected components
cc = graph.connectedComponents()
cc.groupBy("component").count().orderBy("count", ascending=False).show()
```

Witness the intricate tapestry of character connections unveiled before your very eyes! The GraphX sorcery has exposed the hidden alliances, rivalries, and relationships that bind the Seven Kingdoms together.

And there you have it, dear readers! We have traversed the realm of PySpark MLlib, wielding the power of machine learning to unravel the mysteries of the Game of Thrones scripts. From topic modeling to graph analysis, we have explored the Seven Kingdoms in ways even the Maesters of the Citadel could not have foreseen.

But remember, with great power comes great responsibility. Use your PySpark MLlib knowledge wisely, for the fate of Westeros hangs in the balance. May your models be as sharp as Valyrian steel and your insights as profound as the words of the Three-Eyed Raven.

Now, go forth and conquer the world of data, armed with the tools of PySpark MLlib. And always keep a watchful eye on the White Walkers of overfitting and the wildfire of data leakage. Until next time, dear readers, may the Spark be with you!