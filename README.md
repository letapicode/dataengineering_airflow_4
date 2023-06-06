# Data Pipelines with Airflow for Sparkify
## Introduction

Sparkify, a music streaming company, has decided to enhance their data warehouse ETL pipelines by implementing automation and monitoring. They have chosen Apache Airflow as their tool of choice for achieving these goals.

This report documents the process of creating dynamic, reusable, and monitorable data pipelines using Apache Airflow. The solution takes into account Sparkify's requirements for data quality checks and backfill capabilities.

The source data resides in Amazon S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs detailing user activity in the application and JSON metadata about the songs users listen to.

## Project Overview

The project involved creating custom Apache Airflow operators to perform tasks such as staging data, loading data into the data warehouse, and running data quality checks.

## Prerequisites

Before starting the project, an AWS IAM user was created, and Redshift Serverless was configured. Connections were set up in Airflow for AWS and Redshift to enable seamless data processing.


## Project Implementation
### Data Staging
A custom Airflow operator, `StageToRedshiftOperator`, was developed to load JSON-formatted files from S3 to Amazon Redshift. The operator creates and runs a SQL COPY statement based on the parameters provided, specifying the S3 file location and the target table.

### Fact and Dimension Tables
Two custom Airflow operators, `LoadFactOperator` and `LoadDimensionOperator`, were created to handle the loading of fact and dimension tables in Redshift. The operators take a SQL statement and target database as input and use the provided SQL helper class to run data transformations.

The `LoadDimensionOperator` also includes a parameter that allows switching between insert modes (append or truncate-insert) when loading dimensions, as dimension tables are often updated using the truncate-insert pattern.

### Data Quality Checks
A `DataQualityOperator` was created to perform data quality checks on the datasets in Redshift. This operator receives one or more SQL-based test cases along with the expected results and executes the tests. If the test result does not match the expected result, the operator raises an exception, causing the task to retry and eventually fail.

## DAG Configuration and Task Dependencies
The DAG was configured with the following settings:

- No dependencies on past runs
- 3 retries on task failure, with a 5-minute delay between retries
- Catchup turned off
- No email notifications on retry

Task dependencies were set up to ensure a coherent and sensible data flow within the pipeline.

## Results
The implemented data pipeline successfully loads data from S3 to Redshift, transforms and loads fact and dimension tables, and performs data quality checks. The pipeline is dynamic, reusable, and monitorable, meeting Sparkify's requirements for automation and monitoring.

## Conclusion
This project successfully demonstrates the creation of high-grade data pipelines using Apache Airflow. The custom operators developed for the project can be applied to other data pipelines with Redshift or other databases.

By utilizing Airflow's built-in functionalities, Sparkify can now ensure their data warehouse maintains high data quality and can monitor and manage their ETL processes efficiently.


Song Data:
- https://s3-us-west-2.amazonaws.com/udacity-dend/song-data/A/A/A/TRAAAEA128F935A30D.json

Log Data:
- https://s3-us-west-2.amazonaws.com/udacity-dend/log-data/2018/11/2018-11-05-events.json

LogData Path:
- https://s3-us-west-2.amazonaws.com/udacity-dend/log_json_path.json
