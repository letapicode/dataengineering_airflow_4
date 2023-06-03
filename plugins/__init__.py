"""
udacity_plugin.py

This module defines the UdacityPlugin class, which is a custom Airflow plugin for the Udacity data engineering project. The plugin registers custom operators and helpers to be used in Airflow DAGs.

UdacityPlugin Class:
- name: The name of the plugin.
- operators: A list of custom operators provided by the plugin.
- helpers: A list of custom helpers provided by the plugin.

Usage: Include this module in your Airflow plugins directory to make use of the custom operators and helpers in your Airflow DAGs for the Udacity data engineering project.
"""

from __future__ import division, absolute_import, print_function

from airflow.plugins_manager import AirflowPlugin

import operators
import helpers

# Defining the plugin class
class UdacityPlugin(AirflowPlugin):
    name = "udacity_plugin"
    operators = [
        operators.StageToRedshiftOperator,
        operators.LoadFactOperator,
        operators.LoadDimensionOperator,
        operators.DataQualityOperator
    ]
    helpers = [
        helpers.SqlQueries
    ]
