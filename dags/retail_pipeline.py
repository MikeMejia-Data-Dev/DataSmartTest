    import sys
    sys.path.insert(0, '/opt/airflow')

    from datetime import datetime
    from airflow import DAG
    from airflow.providers.standard.operators.python import PythonOperator

    from scripts.init_db import create_schema
    from scripts.extract import extract_all
    from scripts.transform import transform_sales, transform_returns, split_quality_issues_sales
    from scripts.load import load_sales, load_returns, load_rejected
    from scripts.validate import validate_sales, validate_returns

    default_args = {
        "owner": "Mike",
        "retries": 1,
    }

    def run_extract(**context):
        sales, returns = extract_all()
        context['ti'].xcom_push(key='sales', value=sales.to_json())
        context['ti'].xcom_push(key='returns', value=returns.to_json())

    def run_transform(**context):
        import pandas as pd
        sales_json = context['ti'].xcom_pull(task_ids='extract', key='sales')
        returns_json = context['ti'].xcom_pull(task_ids='extract', key='returns')
        
        sales_df = pd.read_json(sales_json)
        returns_df = pd.read_json(returns_json)
        
        transformed_sales = transform_sales(sales_df)
        transformed_returns = transform_returns(returns_df)
        
        context['ti'].xcom_push(key='transformed_sales', value=transformed_sales.to_json())
        context['ti'].xcom_push(key='transformed_returns', value=transformed_returns.to_json())

    def run_validate(**context):
        import pandas as pd
        sales_json = context['ti'].xcom_pull(task_ids='transform', key='transformed_sales')
        returns_json = context['ti'].xcom_pull(task_ids='transform', key='transformed_returns')
        
        sales_df = pd.read_json(sales_json)
        returns_df = pd.read_json(returns_json)
        
        validate_sales(sales_df)
        validate_returns(returns_df)
        
        context['ti'].xcom_push(key='validated_sales', value=sales_df.to_json())
        context['ti'].xcom_push(key='validated_returns', value=returns_df.to_json())

    def run_load(**context):
        import pandas as pd
        from scripts.database import get_engine
        
        sales_json = context['ti'].xcom_pull(task_ids='validate', key='validated_sales')
        returns_json = context['ti'].xcom_pull(task_ids='validate', key='validated_returns')
        
        sales_df = pd.read_json(sales_json)
        returns_df = pd.read_json(returns_json)
        
        engine = get_engine()
        
        valid_sales, rejected_sales = split_quality_issues_sales(sales_df)
        
        load_sales(valid_sales, engine)
        load_returns(returns_df, engine)
        load_rejected(rejected_sales, engine)

    with DAG(
        dag_id="retail_pipeline",
        description="Retail ETL Pipeline",
        start_date=datetime(2026, 1, 1),
        schedule=None,
        catchup=False,
        default_args=default_args,
        tags=["etl", "retail", "postgres"],
    ) as dag:

        create_schema_task = PythonOperator(
            task_id="create_schema",
            python_callable=create_schema,
        )

        extract_task = PythonOperator(
            task_id="extract",
            python_callable=run_extract,
        )

        transform_task = PythonOperator(
            task_id="transform",
            python_callable=run_transform,
        )

        validate_task = PythonOperator(
            task_id="validate",
            python_callable=run_validate,
        )

        load_task = PythonOperator(
            task_id="load",
            python_callable=run_load,
        )

        create_schema_task >> extract_task >> transform_task >> validate_task >> load_task