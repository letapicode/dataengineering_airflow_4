"""
udac_example_dag.py

This DAG script defines the data pipeline for loading and transforming data in Redshift using Apache Airflow. 
The pipeline consists of tasks and operators that perform various ETL operations such as staging data, loading fact and dimension tables, and running data quality checks.

The DAG is scheduled to run hourly and starts with a 'Begin_execution' dummy task and ends with a 'Stop_execution' dummy task.

Tasks:
- create_tables: Task to create the necessary tables in Redshift by executing the 'create_tables.sql' script.
- stage_events_to_redshift: Task to stage event data from S3 to Redshift.
- stage_songs_to_redshift: Task to stage song data from S3 to Redshift.
- load_songplays_table: Task to load the fact table 'songplays' in Redshift by executing the SQL query defined in 'SqlQueries.songplay_table_insert'.
- load_user_dimension_table: Task to load the dimension table 'users' in Redshift by executing the SQL query defined in 'SqlQueries.user_table_insert'.
- load_song_dimension_table: Task to load the dimension table 'songs' in Redshift by executing the SQL query defined in 'SqlQueries.song_table_insert'.
- load_artist_dimension_table: Task to load the dimension table 'artists' in Redshift by executing the SQL query defined in 'SqlQueries.artist_table_insert'.
- load_time_dimension_table: Task to load the dimension table 'time' in Redshift by executing the SQL query defined in 'SqlQueries.time_table_insert'.
- run_quality_checks: Task to run data quality checks on the loaded tables in Redshift.
- end_operator: Dummy task to mark the end of the data pipeline execution.

Note: The SQL queries and table names are imported from 'SqlQueries' and 'plugins.helpers' respectively.

The DAG has default arguments defined and is set to not depend on past runs, with 3 retries on failure, a retry delay of 5 minutes, and catchup disabled.

Usage: This DAG can be scheduled and executed in Apache Airflow to automate the data pipeline for loading and transforming data in Redshift.
"""

from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

from plugins.operators.stage_redshift import StageToRedshiftOperator
from plugins.operators.load_fact import LoadFactOperator
from plugins.operators.load_dimension import LoadDimensionOperator
from plugins.operators.data_quality import DataQualityOperator


from plugins.helpers import SqlQueries


# Define default arguments
default_args = {
    'owner': 'udacity',
    'start_date': datetime(2021, 1, 1),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

# Define DAG
dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval= '@hourly'
        )

# Define tasks and operators
start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

# Create table task
create_tables_task = PostgresOperator(
  task_id="create_tables",
  dag=dag,
  sql='create_tables.sql',
  postgres_conn_id="redshift"
)


stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    table="staging_events",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-dend",
    s3_key="log_data",
    json_path="s3://udacity-dend/log_json_path.json"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    table="staging_songs",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-dend",
    s3_key="song_data", #Test it with 'song_data/A/A/A'
    json_path="auto"
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    table="songplays",
    redshift_conn_id="redshift",
    sql_query=SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    table="users",
    redshift_conn_id="redshift",
    sql_query=SqlQueries.user_table_insert,
    truncate_table=True
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    table="songs",
    redshift_conn_id="redshift",
    sql_query=SqlQueries.song_table_insert,
    truncate_table=True
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    table="artists",
    redshift_conn_id="redshift",
    sql_query=SqlQueries.artist_table_insert,
    truncate_table=True
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    table="time",
    redshift_conn_id="redshift",
    sql_query=SqlQueries.time_table_insert,
    truncate_table=True
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    tables=["songplays", "users", "songs", "artists", "time"],
    redshift_conn_id="redshift"
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# Define task dependencies
start_operator >> create_tables_task
create_tables_task >> [stage_events_to_redshift, stage_songs_to_redshift]
stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table
load_songplays_table >> [load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table]
[load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks
run_quality_checks >> end_operator



