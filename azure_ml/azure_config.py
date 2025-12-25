"""
Azure ML Configuration
Set up connection to Azure Machine Learning workspace
"""

import os
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# ============================================================================
# UPDATE THESE WITH YOUR AZURE DETAILS
# ============================================================================
SUBSCRIPTION_ID = '3c903801-0878-49d9-9d2c-3ed7f0e0ad1c'  # From Azure Portal
RESOURCE_GROUP = 'RG_JIT02'        # Your resource group name
WORKSPACE_NAME = 'cpu-project'        # Your workspace name
LOCATION = "northeurope"                       # Azure region



# Compute resources
COMPUTE_NAME = "cpu-forecast-cluster"
COMPUTE_SKU = "Standard_DS3_v2"
COMPUTE_MIN_NODES = 0
COMPUTE_MAX_NODES = 2

# Model details
MODEL_NAME = "xgboost-cpu-forecaster"
MODEL_VERSION = "1"
ENDPOINT_NAME = "cpu-forecast-endpoint"


def get_ml_client():
    """
    Get authenticated Azure ML client
    Requires Azure CLI login: az login
    """
    credential = DefaultAzureCredential()
    client = MLClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID,
        resource_group_name=RESOURCE_GROUP,
        workspace_name=WORKSPACE_NAME
    )
    return client


def verify_setup():
    """Verify Azure ML workspace is accessible"""
    try:
        client = get_ml_client()
        workspace = client.workspaces.get(WORKSPACE_NAME)
        print(f"✅ Connected to workspace: {workspace.name}")
        print(f"   Region: {workspace.location}")
        print(f"   ID: {workspace.id}")
        return True
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        print("\n📋 Setup steps:")
        print("1. az login")
        print("2. Update SUBSCRIPTION_ID, RESOURCE_GROUP, WORKSPACE_NAME in this file")
        print("3. Create workspace in Azure Portal or using Azure CLI:")
        print("   az ml workspace create -n cpu-forecast-ws -g cpu-forecast-rg")
        return False


if __name__ == "__main__":
    verify_setup()
