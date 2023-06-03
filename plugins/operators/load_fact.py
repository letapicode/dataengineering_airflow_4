"""
load_fact.py

This module contains the LoadFactOperator class, which is a custom operator for loading fact tables in Redshift. The operator inherits from the BaseOperator class provided by Apache Airflow.

LoadFactOperator Class:
- redshift_conn_id: The connection ID for the Redshift connection in Airflow.
- table: The name of the fact table to be loaded.
- sql_query: The SQL query used to insert data into the fact table.

execute() Method:
- Executes the loading of the fact table in Redshift.
- Uses the PostgresHook to establish a connection to Redshift.
- Executes the SQL query to insert data into the fact table.

Usage: Import the LoadFactOperator class from this module to load fact tables in Redshift within your Airflow DAG.
"""

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_query="",
                 *args, **kwargs):
        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info(f"Loading fact table {self.table}")
        insert_query = f"INSERT INTO {self.table} {self.sql_query}"
        redshift.run(insert_query)
