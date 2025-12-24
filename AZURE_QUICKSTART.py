"""
Quick Start Guide for Azure ML Pipeline Setup
"""

# ============================================================================
# STEP-BY-STEP QUICKSTART
# ============================================================================

"""
1. INSTALL AZURE ML SDK
   pip install azure-ai-ml azure-identity
   pip install -r requirements.txt

2. LOGIN TO AZURE
   az login
   
3. CREATE AZURE ML WORKSPACE (if you don't have one)
   
   Option A - Using Portal:
   - Go to portal.azure.com
   - Create "Machine Learning" resource
   - Fill in resource group and workspace name
   
   Option B - Using CLI:
   az group create --name cpu-forecast-rg --location eastus
   az ml workspace create -n cpu-forecast-ws -g cpu-forecast-rg

4. UPDATE azure_config.py
   - Set SUBSCRIPTION_ID (from: az account list --output table)
   - Set RESOURCE_GROUP
   - Set WORKSPACE_NAME
   - Run: python azure_config.py

5. REGISTER MODEL
   python register_model.py

6. CREATE & RUN PIPELINE
   python create_pipeline.py

7. DEPLOY ENDPOINT
   python deploy_endpoint.py

8. TEST ENDPOINT
   python test_endpoint.py
"""

# ============================================================================
# FILE DESCRIPTIONS
# ============================================================================

FILES = {
    "azure_config.py": """
        Configuration and authentication for Azure ML
        - Update with your subscription details
        - Verify connection with: python azure_config.py
    """,
    
    "register_model.py": """
        Upload your trained model to Azure ML
        - Registers xgboost_cpu_forecaster.pkl
        - Adds metadata and properties
    """,
    
    "create_pipeline.py": """
        Define and run ML pipeline with steps:
        1. Data Preparation
        2. Model Training
        3. Model Evaluation
    """,
    
    "deploy_endpoint.py": """
        Deploy model as real-time API endpoint
        - Creates managed online endpoint
        - Deploys model with auto-scaling
    """,
    
    "score.py": """
        Scoring script for endpoint predictions
        - Loads model on startup
        - Handles inference requests
    """,
    
    "prepare_data.py": """
        Pipeline step for data preprocessing
        - Encodes categorical features
        - Creates lag features
        - Calculates time gaps
    """,
    
    "AZURE_ML_SETUP.md": """
        Comprehensive setup documentation
        - Architecture overview
        - Troubleshooting guide
        - Cost estimation
    """
}

# ============================================================================
# QUICK REFERENCE
# ============================================================================

COMMANDS = """
SETUP:
  az login
  python azure_config.py

DEVELOPMENT:
  python register_model.py
  python create_pipeline.py

DEPLOYMENT:
  python deploy_endpoint.py
  python test_endpoint.py

MONITORING:
  Go to: https://ml.azure.com
  Check your workspace dashboard

CLEANUP:
  az ml endpoint delete --name cpu-forecast-endpoint
  az ml workspace delete --name cpu-forecast-ws
"""

# ============================================================================
# IMPORTANT NOTES
# ============================================================================

NOTES = """
✅ BEFORE YOU START:
   - Have an Azure subscription
   - Install Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
   - Run: az login

⚠️  AZURE COSTS:
   - Compute: $10-50/month (depending on usage)
   - Storage: $2-5/month
   - Endpoint: $50-100/month
   - Total estimate: $70-150/month

🔐 SECURITY:
   - Never commit credentials to git
   - Use managed identity for authentication
   - Store secrets in Azure Key Vault

📊 MONITORING:
   - All metrics logged automatically
   - Check Azure Portal for job status
   - Use Application Insights for endpoint monitoring

🚀 BEST PRACTICES:
   - Version your models in Azure ML
   - Use compute quotas to control costs
   - Monitor endpoint latency
   - Track model performance metrics
   - Use auto-scaling for endpoints
"""

if __name__ == "__main__":
    print("=" * 80)
    print("AZURE ML PIPELINE - QUICKSTART GUIDE")
    print("=" * 80)
    
    print("\n📋 FILE DESCRIPTIONS:")
    for file, desc in FILES.items():
        print(f"\n  {file}")
        print(f"  {desc.strip()}")
    
    print("\n" + "=" * 80)
    print("QUICK REFERENCE COMMANDS:")
    print("=" * 80)
    print(COMMANDS)
    
    print("=" * 80)
    print("IMPORTANT NOTES:")
    print("=" * 80)
    print(NOTES)
