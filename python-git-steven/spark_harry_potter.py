import pyspark.sql.functions as F
from pyspark.sql import SparkSession


class SparkHarryPotter:
    def __init__(self):
        self.spark = SparkSession.builder.appName("GameOfThronesAnalysis").getOrCreate()

        self.spark_df = self.spark.read.csv("HarryPotter1.csv", header=True, inferSchema=True)
        # self.psdf = ps.read_csv("HarryPotter1.csv")
        # print("data rows:", spark_df.count())
        # self.psdf = spark_df.pandas_api()
        self.spark_df.describe()

    def analyze(self):
        vector_data, vocabulary = self.__prepare_data(self.spark_df)
        print(vector_data.head(5))

    def __prepare_data(self, data):
        import string
        from nltk.stem.snowball import SnowballStemmer
        from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer
        from pyspark.sql.types import ArrayType, StringType

        tokenizer = Tokenizer(inputCol="Sentence", outputCol="words")
        token_data = tokenizer.transform(data)

        stopwords = StopWordsRemover.loadDefaultStopWords('english')
        stopwords.extend(['it', "I'm", "I", "grace", "your", "yes", "man", "dont", "like", "im", "i'm", "wan", "one"])

        stopwords_remover = StopWordsRemover(inputCol="words", outputCol="filtered_words", stopWords=stopwords)
        # print(stopwords_remover.getStopWords())
        df_no_stopwords = stopwords_remover.transform(token_data)

        def clean_stem(stemmer, token):
            """ Return stem word, removing any punctuation from end of string """
            t = stemmer.stem(token)
            return t.rstrip(string.punctuation)
            # return t.translate(str.maketrans('', '', string.punctuation))

        stemmer = SnowballStemmer(language='english')
        stemmer_udf = F.udf(lambda tokens: [clean_stem(stemmer, token) for token in tokens], ArrayType(StringType()))
        df_stemmed = df_no_stopwords.withColumn("words_stemmed", stemmer_udf("filtered_words"))

        cv = CountVectorizer(inputCol="words_stemmed", outputCol="features")
        cv_model = cv.fit(df_stemmed)
        vocabulary = {i: v for i, v in enumerate(cv_model.vocabulary)}
        vector_data = cv_model.transform(df_stemmed)
        return vector_data, vocabulary


if __name__ == "__main__":
    spark = SparkHarryPotter()
    spark.analyze();
