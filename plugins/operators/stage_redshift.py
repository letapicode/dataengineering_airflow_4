"""
stage_redshift.py

This module contains the StageToRedshiftOperator class, which is a custom operator for staging data from S3 to Redshift. The operator inherits from the BaseOperator class provided by Apache Airflow.

StageToRedshiftOperator Class:
- template_fields: A tuple specifying the template fields used in the operator. In this case, it is set to ("s3_key",).
- copy_sql: The SQL COPY statement template used to copy data from S3 to Redshift.

execute() Method:
- Executes the staging of data from S3 to Redshift.
- Uses the AwsHook to retrieve AWS credentials for Redshift.
- Uses the PostgresHook to establish a connection to Redshift.
- Clears the destination Redshift table by running a DELETE statement.
- Copies the data from S3 to Redshift by running a formatted COPY statement.

Usage: Import the StageToRedshiftOperator class from this module to stage data from S3 to Redshift within your Airflow DAG.
"""


from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    template_fields = ("s3_key",)
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        JSON '{}'
        REGION 'us-west-2'
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 json_path="auto",
                 aws_hook_kwargs=None,
                 *args, **kwargs):
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_path = json_path
        self.aws_credentials_id = aws_credentials_id
        self.aws_hook_kwargs = aws_hook_kwargs or {}

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id, client_type="redshift")
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Clearing data from destination Redshift table")
        redshift.run("DELETE FROM {}".format(self.table))

        self.log.info("Copying data from S3 to Redshift")
        s3_path = "s3://{}/{}".format(self.s3_bucket, self.s3_key.format(**context))
        formatted_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
            self.json_path
        )
        redshift.run(formatted_sql)






