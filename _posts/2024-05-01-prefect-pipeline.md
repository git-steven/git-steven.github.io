---
title:  "Streamlining Data Workflows with Prefect"
date:   2024-05-01 14:40:25 -0500
categories:
- prefect
- data_engineering
- python
- scikit-learn
author: steven
---

_Streamlining Data Workflows with Prefect: A Powerful Alternative to Airflow_

![](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/prefect-md.png)

## Introduction
In the world of data engineering, efficient and reliable data workflows are crucial for managing complex data pipelines. [Prefect](https://www.prefect.io/), a modern workflow management system, has emerged as a powerful alternative to [Apache Airflow](https://airflow.apache.org/), offering a more flexible and intuitive approach to building and executing data workflows.

_What is Prefect?_

[Prefect](https://www.prefect.io/) is an open-source Python library designed to simplify the process of building, scheduling, and monitoring data workflows. It provides a clean and expressive API that allows data engineers to define complex workflows using Python code, making it easy to create, test, and maintain data pipelines.

Prefect vs. Airflow: Similarities and Advantages
[Prefect](https://www.prefect.io/) shares some similarities with [Airflow](https://airflow.apache.org/), as both tools aim to orchestrate and manage data workflows. However, [Prefect](https://www.prefect.io/) offers several advantages over [Airflow](https://airflow.apache.org/):

1. **Python-native:** [Prefect](https://www.prefect.io/) is built around the concept of using pure Python code to define workflows, making it more intuitive and accessible to Python developers.
2. **Task-based approach:** [Prefect](https://www.prefect.io/) introduces the concept of tasks, which are the building blocks of a workflow. Tasks encapsulate a single unit of work and can be easily composed to create complex workflows.
3. **Dynamic flow control:** [Prefect](https://www.prefect.io/) allows for dynamic flow control, enabling tasks to be added, removed, or modified during runtime based on the results of previous tasks.
4. **Concurrency and parallelism:** [Prefect](https://www.prefect.io/) supports concurrent execution of tasks, allowing for efficient utilization of resources and faster execution of workflows.
5. **Advanced error handling:** [Prefect](https://www.prefect.io/) provides a robust error handling mechanism, allowing for automatic retries, failure notifications, and the ability to define custom error handling strategies.

## Dependencies
Before diving into the example code, let's ensure we have the necessary dependencies installed. Here's a list of the required libraries:
- prefect
- prefect-sqlalchemy
- pandas
- numpy
- scikit-learn
- typer

You can install these dependencies using pip:
```bash
pip install prefect prefect-sqlalchemy pandas numpy scikit-learn typer
```

Or, you can follow along using the full working project on [github](https://github.com/terracoil/terracoil-prefect).  
It uses [poetry](https://python-poetry.org/) as a package manager, so you'll need to install that.

### Postgres DB
* Install postgres for your platform if you haven't already. I recommend [homebrew](https://brew.sh/) if you are on OSX.     
* Start up psql and run the following commands

```postgresql
create database prefect_test;
create user prefect with encrypted password 'pr3f3ct';
grant all privileges on database prefect_test to prefect;
```

## About Tasks and Flows
_Understanding Tasks and Flows in Prefect_
In [Prefect](https://www.prefect.io/), a "task" is a Python function decorated with the `@task` decorator. Tasks encapsulate a single unit of work and can take inputs, perform computations, and produce outputs. Tasks are the fundamental building blocks of a Prefect workflow.

A flow, on the other hand, is a collection of tasks arranged in a specific order to accomplish a larger goal. Flows define the dependencies between tasks and specify the order in which they should be executed. Flows are created using the `@flow` decorator in Prefect.

## Example Code
Let's take a closer look at the provided example code and understand how it leverages Prefect for an ETL pipeline.

### Extract
In the `extract_data` task, we use the `connection_context_manager` to establish a connection to the source database. We then execute a SQL query to extract all data from the `source_data` table and return it as a pandas [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

```python
@task
def extract_data() -> DataFrame:
    """
    Extract all data from source_data table into a dataframe
    :return new DataFrame with all data
    """
    logger = get_run_logger()
    logger.info("Extracting data...")

    with connection_context_manager() as connector:
        connection = connector.get_connection(begin=False)
        query = "SELECT * FROM source_data"
        df = pd.read_sql(query, connection)
    return df
```


### Transform
The `transform_data` task takes the extracted [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) as input and performs various data transformations. It applies data cleaning by removing any missing values using `df.dropna(inplace=True)`. It then performs data normalization using [MinMaxScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html#sklearn.preprocessing.MinMaxScaler), standardization using [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html#sklearn.preprocessing.StandardScaler), and Gaussian transformation using [QuantileTransformer](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.QuantileTransformer.html#sklearn.preprocessing.QuantileTransformer) from the [scikit-learn](https://scikit-learn.org/stable/) library.

```python
@task
def transform_data(df: DataFrame) -> DataFrame:
    """
    Transform source data from given DataFrame. Performs cleaning,
    :return transformed data with 3 columns per feature:
        - normalized feature
        - standardized feature
        - Gaussian-transformed feature
    """
    # ...

    # Data normalization
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(df)
    df_normalized = pd.DataFrame(normalized_data, columns=NORMALIZED_COLUMNS)
    df_normalized.drop(columns=['id'], inplace=True)

    # Standardization
    standardized_data = StandardScaler().fit_transform(df)
    df_standardized = pd.DataFrame(standardized_data, columns=STANDARDIZED_COLUMNS)
    df_standardized.drop(columns=['id'], inplace=True)

    # Gaussian transformation
    gaussian_data = QuantileTransformer(output_distribution='normal').fit_transform(df)
    df_gaussian = pd.DataFrame(gaussian_data, columns=GAUSSIAN_COLUMNS)
    df_gaussian.drop(columns=['id'], inplace=True)

    # ...
```

The transformed data is temporarily stored in separate DataFrames (`df_normalized`, `df_standardized`, `df_gaussian`) 
with appropriate column names. These DataFrames are then merged into a single DataFrame `df_xform` before being returned.

## Load
The load task simply stores the transformed data into the `destination_data` table.
```python
@task
def load_data(df_xform) -> None:
    """
    Load transformed data into destination_data table

    :param df_xform: The transformed data to load
    """
    # ...
    with connection_context_manager() as connector:
        connection = connector.get_connection(begin=False)
        df_xform.to_sql('destination_data', connection, if_exists='append', index=False, chunksize=50000)
```

### ETL Pipeline flow

The `etl_pipeline` flow defines the overall ETL process. It calls the `extract_data` task to retrieve the source data, passes it to the `transform_data` task for transformations, and finally calls the `load_data` task to load the transformed data into the destination table.

```python
@flow
def etl_pipeline():
    """
    ETL pipeline flow. Extracts data from source, transforms it, then
    loads it to destination. Transformation step applies data cleaning,
    providing normalized features with MinMaxScaler, standardized features,
    and Gaussian-transformed features using QuantileTransformer.
    """
    df = extract_data()
    df_xform = transform_data(df)
    load_data(df_xform)
```

## Details 

### MinMaxScaler
[MinMaxScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html#sklearn.preprocessing.MinMaxScaler) is a scaling technique that transforms features to a specific range, typically between 0 and 1. It is useful when features have different scales, and you want to bring them to a common scale for comparison or visualization. MinMaxScaler is also beneficial when working with algorithms sensitive to feature scales, such as neural networks or support vector machines. However, it is sensitive to outliers, which can significantly impact the scaling of the features.

### StandardScaler
[StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html#sklearn.preprocessing.StandardScaler) is a scaling technique that standardizes features by removing the mean and scaling to unit variance. It is useful when features have different units or scales, and you want to bring them to a common scale with zero mean and unit variance. StandardScaler is particularly helpful when working with algorithms that assume normally distributed input features, such as linear regression or logistic regression. It gives equal importance to all features, regardless of their original scale. StandardScaler is less sensitive to outliers compared to [MinMaxScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html#sklearn.preprocessing.MinMaxScaler), but extreme outliers can still affect the mean and standard deviation calculations.

### Gaussian distribution
_Leveraging Gaussian Transformation with QuantileTransformer_

In the example code, the `transform_data` task utilizes the [QuantileTransformer](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.QuantileTransformer.html#sklearn.preprocessing.QuantileTransformer) from scikit-learn to perform Gaussian transformation on the input data. The Gaussian transformation aims to transform the data to follow a normal (Gaussian) distribution.

By setting `output_distribution='normal'` in the [QuantileTransformer](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.QuantileTransformer.html#sklearn.preprocessing.QuantileTransformer), the transformed data will have a distribution that approximates a Gaussian distribution. This can be beneficial when working with algorithms that assume normally distributed input data or when you want to reduce the impact of outliers.


## Conclusion
[Prefect](https://www.prefect.io/) offers a powerful and flexible alternative to [Airflow](https://airflow.apache.org/) for building and managing data workflows. With its Python-native approach, task-based composition, dynamic flow control, and advanced error handling capabilities, [Prefect](https://www.prefect.io/) simplifies the process of creating and maintaining complex data pipelines.

By leveraging Prefect's tasks and flows, data engineers can easily define and orchestrate data workflows, incorporating essential data preprocessing techniques like normalization, standardization, and Gaussian transformation using scikit-learn's `QuantileTransformer`. These techniques enhance the quality and compatibility of data, enabling more effective and efficient downstream data processing and analysis tasks.

As data workflows continue to grow in complexity, tools like [Prefect](https://www.prefect.io/) empower data engineers to streamline their workflows, improve data quality, and focus on delivering valuable insights from their data pipelines.