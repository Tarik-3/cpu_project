# Azure ML Commands Reference

Quick reference for common Azure ML operations via CLI and Python SDK.

## 🔐 Authentication

```bash
# Login
az login

# Set default subscription
az account set --subscription "subscription-id"

# List your subscriptions
az account list --output table
```

## 📦 Workspace Management

```bash
# Create resource group
az group create --name cpu-forecast-rg --location eastus

# Create workspace
az ml workspace create \
  --name cpu-forecast-ws \
  --resource-group cpu-forecast-rg \
  --location eastus

# List workspaces
az ml workspace list --resource-group cpu-forecast-rg

# Get workspace details
az ml workspace show --name cpu-forecast-ws --resource-group cpu-forecast-rg
```

## 🖥️ Compute Management

```bash
# Create compute cluster
az ml compute create \
  --name cpu-forecast-cluster \
  --type amlcompute \
  --min-instances 0 \
  --max-instances 2 \
  --size Standard_DS3_v2 \
  --resource-group cpu-forecast-rg \
  --workspace-name cpu-forecast-ws

# List compute
az ml compute list --workspace-name cpu-forecast-ws

# Delete compute
az ml compute delete \
  --name cpu-forecast-cluster \
  --workspace-name cpu-forecast-ws
```

## 📊 Data Management

```bash
# Upload data
az ml data create \
  --name cpu-data \
  --version 1 \
  --type uri_file \
  --path data.csv \
  --workspace-name cpu-forecast-ws

# List datasets
az ml data list --workspace-name cpu-forecast-ws

# Download data
az ml data download \
  --name cpu-data \
  --version 1 \
  --download-path ./
```

## 🤖 Model Management

```bash
# Register model
az ml model create \
  --name xgboost-cpu-forecaster \
  --version 1 \
  --path xgboost_cpu_forecaster.pkl \
  --type custom_model \
  --workspace-name cpu-forecast-ws

# List models
az ml model list --workspace-name cpu-forecast-ws

# Get model details
az ml model show \
  --name xgboost-cpu-forecaster \
  --version 1 \
  --workspace-name cpu-forecast-ws

# Download model
az ml model download \
  --name xgboost-cpu-forecaster \
  --version 1 \
  --download-path ./models/
```

## 📋 Job/Run Management

```bash
# List jobs
az ml job list --workspace-name cpu-forecast-ws

# Get job details
az ml job show --name <job-id> --workspace-name cpu-forecast-ws

# Stream job logs
az ml job stream --name <job-id> --workspace-name cpu-forecast-ws

# Cancel job
az ml job cancel --name <job-id> --workspace-name cpu-forecast-ws
```

## 🌐 Endpoint Management

```bash
# Create endpoint
az ml online-endpoint create \
  --file endpoint.yml \
  --workspace-name cpu-forecast-ws

# List endpoints
az ml online-endpoint list --workspace-name cpu-forecast-ws

# Get endpoint details
az ml online-endpoint show \
  --name cpu-forecast-endpoint \
  --workspace-name cpu-forecast-ws

# Get endpoint keys
az ml online-endpoint get-credentials \
  --name cpu-forecast-endpoint \
  --workspace-name cpu-forecast-ws

# Delete endpoint
az ml online-endpoint delete \
  --name cpu-forecast-endpoint \
  --workspace-name cpu-forecast-ws
```

## 📝 Deployment Management

```bash
# Create deployment
az ml online-deployment create \
  --file deployment.yml \
  --endpoint-name cpu-forecast-endpoint \
  --workspace-name cpu-forecast-ws

# List deployments
az ml online-deployment list \
  --endpoint-name cpu-forecast-endpoint \
  --workspace-name cpu-forecast-ws

# Update deployment
az ml online-deployment update \
  --name cpu-forecast-deployment \
  --endpoint-name cpu-forecast-endpoint \
  --file deployment.yml

# Delete deployment
az ml online-deployment delete \
  --name cpu-forecast-deployment \
  --endpoint-name cpu-forecast-endpoint
```

## 🧪 Testing

```bash
# Test endpoint locally
az ml online-endpoint invoke \
  --name cpu-forecast-endpoint \
  --request-file test_data.json \
  --workspace-name cpu-forecast-ws

# Test with curl
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d @test_data.json \
  <scoring-uri>
```

## 📊 Monitoring & Logs

```bash
# Get endpoint metrics
az monitor metrics list \
  --resource cpu-forecast-endpoint \
  --resource-group cpu-forecast-rg

# Stream logs
az ml job stream --name <job-id>

# Get full logs
az ml job download --name <job-id> --output-name logs
```

## 🔨 Environment Management

```bash
# Create environment
az ml environment create \
  --file environments/env_cpu_forecast.yml \
  --workspace-name cpu-forecast-ws

# List environments
az ml environment list --workspace-name cpu-forecast-ws

# Download environment
az ml environment download \
  --name cpu-forecast-env \
  --version 1 \
  --download-path ./
```

## 🗑️ Cleanup

```bash
# Delete workspace (WARNING: irreversible)
az ml workspace delete \
  --name cpu-forecast-ws \
  --resource-group cpu-forecast-rg

# Delete resource group (WARNING: deletes all resources)
az group delete --name cpu-forecast-rg

# Delete individual resources
az ml model delete --name xgboost-cpu-forecaster
az ml online-endpoint delete --name cpu-forecast-endpoint
az ml compute delete --name cpu-forecast-cluster
```

## 📈 Useful Dashboard URLs

Replace `<workspace>` and `<subscription>` with your values:

```
Workspace: https://ml.azure.com/workspaces/<workspace>
Jobs: https://ml.azure.com/workspaces/<workspace>/jobs
Models: https://ml.azure.com/workspaces/<workspace>/models
Datasets: https://ml.azure.com/workspaces/<workspace>/data
Endpoints: https://ml.azure.com/workspaces/<workspace>/endpoints
```

## 💡 Useful Tips

1. **Save default values in config**:
   ```bash
   az configure --defaults group=cpu-forecast-rg workspace=cpu-forecast-ws
   ```

2. **Export job output**:
   ```bash
   az ml job download --name <job-id> --all
   ```

3. **Get real-time logs**:
   ```bash
   watch -n 5 'az ml job show --name <job-id> | grep status'
   ```

4. **Quick job submission**:
   ```bash
   az ml job create --file job.yml --workspace-name cpu-forecast-ws
   ```

## 🚀 Common Workflows

### Deploy New Model Version

```bash
# Register new model
az ml model create --name xgboost-cpu-forecaster --version 2 --path new_model.pkl

# Update deployment to use new version
az ml online-deployment update \
  --name cpu-forecast-deployment \
  --endpoint-name cpu-forecast-endpoint \
  --model xgboost-cpu-forecaster:2
```

### Monitor Endpoint Health

```bash
# Check endpoint status
az ml online-endpoint show --name cpu-forecast-endpoint

# Get deployment logs
az ml online-deployment get-logs \
  --name cpu-forecast-deployment \
  --endpoint-name cpu-forecast-endpoint
```

### Scale Endpoint

```bash
# Increase instances
az ml online-deployment update \
  --name cpu-forecast-deployment \
  --endpoint-name cpu-forecast-endpoint \
  --instance-count 3

# Decrease instances
az ml online-deployment update \
  --name cpu-forecast-deployment \
  --endpoint-name cpu-forecast-endpoint \
  --instance-count 1
```

## 🔗 Related Documentation

- [Azure ML CLI Reference](https://learn.microsoft.com/en-us/cli/azure/ml)
- [Azure ML Python SDK](https://aka.ms/aml-sdk)
- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)
