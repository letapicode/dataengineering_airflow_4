"""
data_quality.py

This module contains the DataQualityOperator class, which is a custom operator for performing data quality checks on tables in Redshift. The operator inherits from the BaseOperator class provided by Apache Airflow.

DataQualityOperator Class:
- redshift_conn_id: The connection ID for the Redshift connection in Airflow.
- tables: A list of table names on which data quality checks will be performed.

execute() Method:
- Executes the data quality checks on the specified tables.
- Uses the PostgresHook to establish a connection to Redshift.
- Retrieves the count of records for each table and checks if the count is valid.
- Raises a ValueError if the data quality check fails.

Usage: Import the DataQualityOperator class from this module to perform data quality checks on tables in Redshift within your Airflow DAG.
"""

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables=None,
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        if tables is None:
            tables = []
        self.tables = tables

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        for table in self.tables:
            self.log.info(f"Running data quality check on {table}")
            records = redshift.get_records(f"SELECT COUNT(*) FROM {table}")

            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. {table} returned no results")
            num_records = records[0][0]
            if num_records < 1:
                raise ValueError(f"Data quality check failed. {table} contained 0 rows")

        self.log.info("Data quality checks passed")
