"""
operators/__init__.py

This module initializes the operators package and lists the available operators for data pipeline tasks. The available operators are as follows:

- StageToRedshiftOperator: Custom operator for staging data from S3 to Redshift.
- LoadFactOperator: Custom operator for loading fact tables in Redshift.
- LoadDimensionOperator: Custom operator for loading dimension tables in Redshift.
- DataQualityOperator: Custom operator for performing data quality checks on tables in Redshift.

__all__:
- A list of the available operators, which can be imported using the wildcard import from the operators package.

Usage: Import the desired operators from this module to use them in your Airflow DAG for data pipeline tasks.
"""

from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality import DataQualityOperator

__all__ = [
    'StageToRedshiftOperator',
    'LoadFactOperator',
    'LoadDimensionOperator',
    'DataQualityOperator'
]
