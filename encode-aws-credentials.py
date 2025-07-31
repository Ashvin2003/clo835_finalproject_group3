#!/usr/bin/env python3
"""
Helper script to encode AWS credentials for Kubernetes secrets.
Run this script to get base64 encoded values for your aws-secret.yaml file.
"""

import base64
import sys

def encode_credentials():
    print("AWS Credentials Encoder for Kubernetes Secrets")
    print("=" * 50)
    
    # Get credentials from user
    access_key_id = input("Enter your AWS Access Key ID: ").strip()
    secret_access_key = input("Enter your AWS Secret Access Key: ").strip()
    session_token = input("Enter your AWS Session Token (optional, press Enter if none): ").strip()
    
    if not access_key_id or not secret_access_key:
        print("Error: Access Key ID and Secret Access Key are required!")
        sys.exit(1)
    
    # Encode credentials
    encoded_access_key = base64.b64encode(access_key_id.encode()).decode()
    encoded_secret_key = base64.b64encode(secret_access_key.encode()).decode()
    encoded_session_token = base64.b64encode(session_token.encode()).decode() if session_token else ""
    
    print("\n" + "=" * 50)
    print("Base64 Encoded Credentials:")
    print("=" * 50)
    print(f"aws-access-key-id: {encoded_access_key}")
    print(f"aws-secret-access-key: {encoded_secret_key}")
    if encoded_session_token:
        print(f"aws-session-token: {encoded_session_token}")
    else:
        print("aws-session-token: <empty>")
    
    print("\n" + "=" * 50)
    print("Update your k8s/aws-secret.yaml file with these values!")
    print("=" * 50)

if __name__ == "__main__":
    encode_credentials() 