import os
import requests
import subprocess

# Apigee Edge API credentials
APIGEE_ORG = 'your_org_name'
APIGEE_ENV = 'your_environment'
APIGEE_USERNAME = 'your_username'
APIGEE_PASSWORD = 'your_password'

# OpenAPI Specification URL
OPENAPI_SPEC_URL = 'https://example.com/openapi.yaml'  # Replace with your OpenAPI spec URL

# Directory to store generated Apigee proxy bundle
PROXY_BUNDLE_DIR = 'proxy_bundle'

# Apigee API base URL
APIGEE_BASE_URL = f'https://api.enterprise.apigee.com/v1/organizations/{APIGEE_ORG}/'

# Step 1: Download the OpenAPI specification
def download_openapi_spec():
    response = requests.get(OPENAPI_SPEC_URL)
    if response.status_code == 200:
        with open('openapi.yaml', 'wb') as f:
            f.write(response.content)
    else:
        print(f'Failed to download OpenAPI spec. Status Code: {response.status_code}, Response: {response.text}')
        exit(1)

# Step 2: Use openai-cli to generate Apigee proxy
def generate_apigee_proxy():
    download_openapi_spec()

    # Use openai-cli to generate the Apigee proxy
    try:
        subprocess.run(['openai-cli', 'apigee', 'generate', 'openapi.yaml', '--out', PROXY_BUNDLE_DIR], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Failed to generate Apigee proxy. Error: {e}')
        exit(1)

# Step 3: Create Apigee proxy
def create_apigee_proxy():
    proxy_name = 'your_proxy_name'

    # Create a new proxy in Apigee
    proxy_create_url = f'{APIGEE_BASE_URL}apis'
    headers = {
        'Content-Type': 'application/json',
    }
    proxy_data = {
        'name': proxy_name,
        'revision': '1',  # Specify the revision number
        'openapi': f'{OPENAPI_SPEC_URL}',
    }

    response = requests.post(proxy_create_url, headers=headers, json=proxy_data, auth=(APIGEE_USERNAME, APIGEE_PASSWORD))

    if response.status_code == 201:
        print(f'Successfully created Apigee proxy: {proxy_name}')
    else:
        print(f'Failed to create Apigee proxy. Status Code: {response.status_code}, Response: {response.text}')
        exit(1)

# Step 4: Deploy Apigee proxy
def deploy_apigee_proxy():
    proxy_name = 'your_proxy_name'
    proxy_revision = '1'  # Specify the revision number

    # Deploy the Apigee proxy
    deploy_url = f'{APIGEE_BASE_URL}apis/{proxy_name}/revisions/{proxy_revision}/deployments'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post(deploy_url, headers=headers, auth=(APIGEE_USERNAME, APIGEE_PASSWORD))

    if response.status_code == 200:
        print(f'Successfully deployed Apigee proxy: {proxy_name} (Revision: {proxy_revision})')
    else:
        print(f'Failed to deploy Apigee proxy. Status Code: {response.status_code}, Response: {response.text}')
        exit(1)

if __name__ == '__main__':
    generate_apigee_proxy()
    create_apigee_proxy()
    deploy_apigee_proxy()
