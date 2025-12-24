#!/usr/bin/env python3
"""
Azure ML Deployment - Interactive Checklist
Run this to verify your setup step by step
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and check if it succeeds"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description}")
            print(f"   Error: {result.stderr[:100]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏱️  {description} (timeout)")
        return False
    except Exception as e:
        print(f"❌ {description} - {str(e)}")
        return False


def check_prerequisites():
    """Check all prerequisites"""
    print("\n" + "="*60)
    print("PREREQUISITE CHECKS")
    print("="*60 + "\n")
    
    checks = [
        ("python --version", "Python installed"),
        ("az --version", "Azure CLI installed"),
        ("pip list | findstr azure-ai-ml", "Azure ML SDK installed"),
        ("git --version", "Git installed"),
    ]
    
    results = []
    for cmd, desc in checks:
        results.append(run_command(cmd, desc))
    
    return all(results)


def check_azure_setup():
    """Check Azure configuration"""
    print("\n" + "="*60)
    print("AZURE SETUP CHECKS")
    print("="*60 + "\n")
    
    checks = [
        ("az account show", "Azure login verified"),
    ]
    
    results = []
    for cmd, desc in checks:
        results.append(run_command(cmd, desc))
    
    return all(results)


def check_configuration():
    """Check configuration file"""
    print("\n" + "="*60)
    print("CONFIGURATION CHECKS")
    print("="*60 + "\n")
    
    config_file = Path("azure_config.py")
    
    if not config_file.exists():
        print("❌ azure_config.py not found")
        return False
    
    with open(config_file) as f:
        content = f.read()
    
    checks = [
        ("SUBSCRIPTION_ID" in content and "YOUR-SUBSCRIPTION" not in content, 
         "SUBSCRIPTION_ID configured"),
        ("RESOURCE_GROUP" in content, "RESOURCE_GROUP configured"),
        ("WORKSPACE_NAME" in content, "WORKSPACE_NAME configured"),
    ]
    
    results = []
    for check, desc in checks:
        if check:
            print(f"✅ {desc}")
            results.append(True)
        else:
            print(f"⚠️  {desc} (verify in azure_config.py)")
            results.append(False)
    
    return all(results)


def check_files():
    """Check all required files exist"""
    print("\n" + "="*60)
    print("FILE CHECKS")
    print("="*60 + "\n")
    
    required_files = [
        "server.py",
        "test.py",
        "azure_config.py",
        "register_model.py",
        "create_pipeline.py",
        "deploy_endpoint.py",
        "score.py",
        "prepare_data.py",
        "xgboost_cpu_forecaster.pkl",
        "data.csv",
        "requirements.txt",
    ]
    
    results = []
    for file in required_files:
        exists = Path(file).exists()
        status = "✅" if exists else "❌"
        print(f"{status} {file}")
        results.append(exists)
    
    return all(results)


def show_next_steps():
    """Show next steps"""
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60 + "\n")
    
    steps = [
        ("1", "Update azure_config.py", "Edit SUBSCRIPTION_ID, RESOURCE_GROUP, WORKSPACE_NAME"),
        ("2", "Verify Azure connection", "python azure_config.py"),
        ("3", "Register model", "python register_model.py"),
        ("4", "Create pipeline", "python create_pipeline.py"),
        ("5", "Deploy endpoint", "python deploy_endpoint.py"),
        ("6", "Test endpoint", "Automatic test at end of deploy_endpoint.py"),
    ]
    
    for num, task, cmd in steps:
        print(f"Step {num}: {task}")
        print(f"  → {cmd}\n")


def show_useful_links():
    """Show useful links"""
    print("\n" + "="*60)
    print("USEFUL LINKS")
    print("="*60 + "\n")
    
    links = [
        ("Azure Portal", "https://portal.azure.com"),
        ("Azure ML Studio", "https://ml.azure.com"),
        ("Azure ML Docs", "https://learn.microsoft.com/en-us/azure/machine-learning/"),
        ("Python SDK Docs", "https://learn.microsoft.com/en-us/python/api/azure-ai-ml/"),
        ("CLI Reference", "https://learn.microsoft.com/en-us/cli/azure/ml"),
    ]
    
    for name, url in links:
        print(f"📌 {name}")
        print(f"   {url}\n")


def show_troubleshooting():
    """Show common troubleshooting tips"""
    print("\n" + "="*60)
    print("TROUBLESHOOTING QUICK REFERENCE")
    print("="*60 + "\n")
    
    issues = [
        ("Auth fails", "Run: az login"),
        ("Command not found", "Install: pip install azure-ai-ml azure-identity"),
        ("Import error", "Check Python path: which python"),
        ("Quota exceeded", "Increase in Azure Portal → Quotas"),
        ("Endpoint timeout", "Increase timeout value in deploy_endpoint.py"),
    ]
    
    for issue, solution in issues:
        print(f"❓ {issue}")
        print(f"   💡 {solution}\n")


def main():
    """Run all checks"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "AZURE ML DEPLOYMENT - SETUP CHECKER" + " "*12 + "║")
    print("╚" + "="*58 + "╝")
    
    all_passed = True
    
    # Run checks
    if not check_prerequisites():
        print("\n⚠️  Some prerequisites are missing. Please install them.")
        all_passed = False
    
    if not check_azure_setup():
        print("\n❌ Azure setup incomplete. Run: az login")
        all_passed = False
    
    if not check_configuration():
        print("\n⚠️  Configuration needs review")
    
    if not check_files():
        print("\n❌ Some files are missing")
        all_passed = False
    
    # Show guidance
    show_next_steps()
    show_useful_links()
    show_troubleshooting()
    
    # Summary
    print("="*60)
    if all_passed:
        print("✅ All checks passed! Ready to deploy.")
        print("\nStart with: python azure_config.py")
    else:
        print("⚠️  Please address the issues above before deploying.")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup checker cancelled.")
        sys.exit(0)
