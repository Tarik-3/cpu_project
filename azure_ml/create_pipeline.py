"""
Create and run Azure ML Pipeline
"""

from azure.ai.ml import MLClient, dsl, Input, Output
from azure.ai.ml.entities import Environment
from azure.ai.ml.constants import AssetTypes
import os
from azure_config import (
    get_ml_client, COMPUTE_NAME, MODEL_NAME, 
    MODEL_VERSION, LOCATION, RESOURCE_GROUP
)


def create_pipeline():
    """
    Create a machine learning pipeline with multiple steps:
    1. Data Preparation (preprocess raw data)
    2. Model Training (train XGBoost)
    3. Model Evaluation (calculate metrics)
    4. Model Registration (register to Azure ML)
    """
    
    client = get_ml_client()
    
    # Get compute cluster (create if doesn't exist)
    print(f"Setting up compute cluster: {COMPUTE_NAME}")
    try:
        compute = client.compute.get(COMPUTE_NAME)
        print(f"✅ Compute cluster exists: {compute.name}")
    except:
        print(f"Creating compute cluster...")
        from azure.ai.ml.entities import AmlCompute
        compute = AmlCompute(
            name=COMPUTE_NAME,
            type="amlcompute",
            size="Standard_DS3_v2",
            min_instances=0,
            max_instances=2,
            idle_time_before_scale_down=120,
            location=LOCATION
        )
        client.compute.begin_create_or_update(compute).result()
        print(f"✅ Compute cluster created")
    
    # Create environment with dependencies
    print("Setting up Python environment...")
    env = Environment(
        name="cpu-forecast-env",
        conda_file="environments/env_cpu_forecast.yml",
        image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04"
    )
    env = client.environments.create_or_update(env)
    print(f"✅ Environment ready: {env.name}")
    
    # Define pipeline steps
    @dsl.pipeline(
        compute=COMPUTE_NAME,
        description="CPU Usage Forecasting Pipeline",
        name="cpu-forecast-pipeline"
    )
    def cpu_forecast_pipeline():
        """Pipeline for CPU forecasting model"""
        
        # Step 1: Data Preparation
        print("Defining data preparation step...")
        prepare_step = dsl.command(
            command="""
            python prepare_data.py \
                --input_data ${{inputs.raw_data}} \
                --output_data ${{outputs.prepared_data}}
            """,
            inputs={
                "raw_data": Input(type=AssetTypes.URI_FILE, path="data.csv")
            },
            outputs={
                "prepared_data": Output(type=AssetTypes.URI_FILE)
            },
            environment=env,
            compute=COMPUTE_NAME,
            code="./",
        )
        
        # Step 2: Model Training
        print("Defining training step...")
        train_step = dsl.command(
            command="""
            python train_model.py \
                --input_data ${{inputs.training_data}} \
                --model_path ${{outputs.model}} \
                --metrics_path ${{outputs.metrics}}
            """,
            inputs={
                "training_data": prepare_step.outputs.prepared_data
            },
            outputs={
                "model": Output(type=AssetTypes.CUSTOM_MODEL),
                "metrics": Output(type=AssetTypes.URI_FILE)
            },
            environment=env,
            compute=COMPUTE_NAME,
            code="./",
        )
        
        # Step 3: Model Evaluation
        print("Defining evaluation step...")
        eval_step = dsl.command(
            command="""
            python evaluate_model.py \
                --model_path ${{inputs.model}} \
                --test_data ${{inputs.test_data}} \
                --eval_results ${{outputs.eval_results}}
            """,
            inputs={
                "model": train_step.outputs.model,
                "test_data": prepare_step.outputs.prepared_data
            },
            outputs={
                "eval_results": Output(type=AssetTypes.URI_FILE)
            },
            environment=env,
            compute=COMPUTE_NAME,
            code="./",
        )
        
        return {
            "pipeline_model": train_step.outputs.model,
            "pipeline_metrics": train_step.outputs.metrics,
            "pipeline_eval": eval_step.outputs.eval_results
        }
    
    # Create the pipeline
    print("\n🔄 Creating pipeline...")
    pipeline = cpu_forecast_pipeline()
    
    return pipeline


def run_pipeline():
    """Submit pipeline job to Azure ML"""
    
    client = get_ml_client()
    
    # Create pipeline
    pipeline_job = create_pipeline()
    
    # Submit job
    print("\n📤 Submitting pipeline job...")
    submitted_job = client.jobs.create_or_update(pipeline_job)
    
    print(f"✅ Pipeline submitted!")
    print(f"   Job ID: {submitted_job.name}")
    print(f"   Status: {submitted_job.status}")
    
    # Monitor progress
    print("\n⏳ Monitoring pipeline execution...")
    print("   Check progress at: https://ml.azure.com/jobs/{}/details".format(submitted_job.name))
    
    # Wait for completion
    client.jobs.stream(submitted_job.name)
    
    # Get final results
    completed_job = client.jobs.get(submitted_job.name)
    print(f"\n✅ Pipeline completed with status: {completed_job.status}")
    
    return completed_job


if __name__ == "__main__":
    pipeline_job = run_pipeline()
