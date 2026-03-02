#!/usr/bin/env python3
"""
Infrastructure Verification Script

This script verifies that all required AWS infrastructure components are properly set up:
- DynamoDB tables (8 tables)
- S3 buckets (3 buckets)
- Cognito User Pool
- API Gateway endpoints
- ElastiCache Redis cluster (optional)
- CloudFront distribution (optional)

Usage:
    python verify_infrastructure.py
    python verify_infrastructure.py --prefix voice-for-bharat-dev
    python verify_infrastructure.py --skip-optional
"""

import argparse
import boto3
import sys
from typing import Dict, List, Tuple
from botocore.exceptions import ClientError


# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text: str):
    """Print section header"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{GREEN}✓{RESET} {text}")


def print_error(text: str):
    """Print error message"""
    print(f"{RED}✗{RESET} {text}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{YELLOW}⚠{RESET} {text}")


def print_info(text: str):
    """Print info message"""
    print(f"  {text}")


# Expected DynamoDB tables
EXPECTED_TABLES = [
    "users",
    "schemes",
    "applications",
    "activity-log",
    "user-profile",
    "helplines",
    "guide-content",
    "suggested-queries"
]


# Expected S3 buckets (without account ID suffix)
EXPECTED_BUCKETS = [
    "documents",
    "audio",
    "scheme-dumps"
]


def verify_dynamodb_tables(prefix: str) -> Tuple[bool, List[str]]:
    """Verify all DynamoDB tables exist and are active"""
    print_header("Verifying DynamoDB Tables")
    
    client = boto3.client('dynamodb')
    errors = []
    success_count = 0
    
    for table_short_name in EXPECTED_TABLES:
        table_name = f"{prefix}-{table_short_name}"
        
        try:
            response = client.describe_table(TableName=table_name)
            table_info = response.get('Table', {})
            status = table_info.get('TableStatus')
            item_count = table_info.get('ItemCount', 0)
            
            if status == 'ACTIVE':
                print_success(f"{table_short_name:20} - Status: {status}, Items: {item_count:,}")
                success_count += 1
            else:
                print_warning(f"{table_short_name:20} - Status: {status} (not ACTIVE)")
                errors.append(f"Table {table_name} is not ACTIVE (status: {status})")
                
        except client.exceptions.ResourceNotFoundException:
            print_error(f"{table_short_name:20} - NOT FOUND")
            errors.append(f"Table {table_name} does not exist")
        except Exception as e:
            print_error(f"{table_short_name:20} - ERROR: {str(e)}")
            errors.append(f"Error checking table {table_name}: {str(e)}")
    
    print(f"\n{success_count}/{len(EXPECTED_TABLES)} tables found and active")
    
    return len(errors) == 0, errors


def verify_s3_buckets(prefix: str, environment: str) -> Tuple[bool, List[str]]:
    """Verify all S3 buckets exist"""
    print_header("Verifying S3 Buckets")
    
    s3_client = boto3.client('s3')
    sts_client = boto3.client('sts')
    
    # Get account ID
    try:
        account_id = sts_client.get_caller_identity()['Account']
    except Exception as e:
        print_error(f"Could not get AWS account ID: {e}")
        return False, [f"Could not get AWS account ID: {e}"]
    
    errors = []
    success_count = 0
    
    for bucket_type in EXPECTED_BUCKETS:
        bucket_name = f"voice-for-bharat-{bucket_type}-{environment}-{account_id}"
        
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            
            # Check encryption
            try:
                encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
                encrypted = True
            except ClientError as e:
                if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                    encrypted = False
                else:
                    encrypted = None
            
            # Check versioning (for documents and scheme-dumps)
            versioning_status = "N/A"
            if bucket_type in ["documents", "scheme-dumps"]:
                try:
                    versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
                    versioning_status = versioning.get('Status', 'Disabled')
                except Exception:
                    versioning_status = "Unknown"
            
            status_text = f"Encrypted: {encrypted}, Versioning: {versioning_status}"
            print_success(f"{bucket_type:20} - {status_text}")
            success_count += 1
            
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                print_error(f"{bucket_type:20} - NOT FOUND")
                errors.append(f"Bucket {bucket_name} does not exist")
            else:
                print_error(f"{bucket_type:20} - ERROR: {str(e)}")
                errors.append(f"Error checking bucket {bucket_name}: {str(e)}")
        except Exception as e:
            print_error(f"{bucket_type:20} - ERROR: {str(e)}")
            errors.append(f"Error checking bucket {bucket_name}: {str(e)}")
    
    print(f"\n{success_count}/{len(EXPECTED_BUCKETS)} buckets found")
    
    return len(errors) == 0, errors


def verify_cognito_user_pool(prefix: str, environment: str) -> Tuple[bool, List[str]]:
    """Verify Cognito User Pool exists"""
    print_header("Verifying Cognito User Pool")
    
    client = boto3.client('cognito-idp')
    errors = []
    
    try:
        # List all user pools and find ours
        response = client.list_user_pools(MaxResults=60)
        user_pools = response.get('UserPools', [])
        
        pool_name = f"voice-for-bharat-users-{environment}"
        matching_pool = None
        
        for pool in user_pools:
            if pool['Name'] == pool_name:
                matching_pool = pool
                break
        
        if matching_pool:
            pool_id = matching_pool['Id']
            
            # Get detailed info
            pool_details = client.describe_user_pool(UserPoolId=pool_id)
            pool_info = pool_details.get('UserPool', {})
            
            status = pool_info.get('Status', 'Unknown')
            user_count = pool_info.get('EstimatedNumberOfUsers', 0)
            
            print_success(f"User Pool: {pool_name}")
            print_info(f"Pool ID: {pool_id}")
            print_info(f"Status: {status}")
            print_info(f"Users: {user_count:,}")
            
            # Check MFA configuration
            mfa_config = pool_info.get('MfaConfiguration', 'OFF')
            print_info(f"MFA: {mfa_config}")
            
            return True, []
        else:
            print_error(f"User Pool '{pool_name}' not found")
            errors.append(f"Cognito User Pool '{pool_name}' does not exist")
            return False, errors
            
    except Exception as e:
        print_error(f"Error checking Cognito User Pool: {str(e)}")
        errors.append(f"Error checking Cognito User Pool: {str(e)}")
        return False, errors


def verify_api_gateway(prefix: str, environment: str) -> Tuple[bool, List[str]]:
    """Verify API Gateway exists"""
    print_header("Verifying API Gateway")
    
    client = boto3.client('apigateway')
    errors = []
    
    try:
        # List all REST APIs
        response = client.get_rest_apis(limit=500)
        apis = response.get('items', [])
        
        api_name = f"voice-for-bharat-api-{environment}"
        matching_api = None
        
        for api in apis:
            if api['name'] == api_name:
                matching_api = api
                break
        
        if matching_api:
            api_id = matching_api['id']
            
            print_success(f"REST API: {api_name}")
            print_info(f"API ID: {api_id}")
            print_info(f"Endpoint: https://{api_id}.execute-api.{boto3.session.Session().region_name}.amazonaws.com/{environment}")
            
            # Try to get resources
            try:
                resources = client.get_resources(restApiId=api_id, limit=500)
                resource_count = len(resources.get('items', []))
                print_info(f"Resources: {resource_count}")
            except Exception:
                pass
            
            return True, []
        else:
            print_warning(f"REST API '{api_name}' not found (may not be deployed yet)")
            errors.append(f"API Gateway '{api_name}' does not exist")
            return False, errors
            
    except Exception as e:
        print_error(f"Error checking API Gateway: {str(e)}")
        errors.append(f"Error checking API Gateway: {str(e)}")
        return False, errors


def verify_elasticache(prefix: str, environment: str) -> Tuple[bool, List[str]]:
    """Verify ElastiCache Redis cluster (optional)"""
    print_header("Verifying ElastiCache Redis Cluster (Optional)")
    
    client = boto3.client('elasticache')
    errors = []
    
    try:
        cluster_id = f"voice-for-bharat-redis-{environment}"
        
        response = client.describe_cache_clusters(
            CacheClusterId=cluster_id,
            ShowCacheNodeInfo=True
        )
        
        clusters = response.get('CacheClusters', [])
        
        if clusters:
            cluster = clusters[0]
            status = cluster.get('CacheClusterStatus')
            node_type = cluster.get('CacheNodeType')
            engine = cluster.get('Engine')
            
            print_success(f"Redis Cluster: {cluster_id}")
            print_info(f"Status: {status}")
            print_info(f"Node Type: {node_type}")
            print_info(f"Engine: {engine}")
            
            # Get endpoint
            if cluster.get('CacheNodes'):
                endpoint = cluster['CacheNodes'][0].get('Endpoint', {})
                address = endpoint.get('Address')
                port = endpoint.get('Port')
                if address:
                    print_info(f"Endpoint: {address}:{port}")
            
            return True, []
        else:
            print_warning(f"Redis cluster '{cluster_id}' not found (optional component)")
            return True, []  # Not an error since it's optional
            
    except client.exceptions.CacheClusterNotFoundFault:
        print_warning(f"Redis cluster not found (optional component)")
        return True, []  # Not an error since it's optional
    except Exception as e:
        print_warning(f"Could not verify Redis cluster: {str(e)}")
        return True, []  # Not an error since it's optional


def verify_cloudfront(environment: str) -> Tuple[bool, List[str]]:
    """Verify CloudFront distribution (optional)"""
    print_header("Verifying CloudFront Distribution (Optional)")
    
    client = boto3.client('cloudfront')
    errors = []
    
    try:
        response = client.list_distributions()
        distributions = response.get('DistributionList', {}).get('Items', [])
        
        # Look for distribution with our comment
        comment_prefix = f"Voice for Bharat CDN {environment}"
        matching_dist = None
        
        for dist in distributions:
            if dist.get('Comment', '').startswith(comment_prefix):
                matching_dist = dist
                break
        
        if matching_dist:
            dist_id = matching_dist['Id']
            domain_name = matching_dist['DomainName']
            status = matching_dist['Status']
            
            print_success(f"CloudFront Distribution found")
            print_info(f"Distribution ID: {dist_id}")
            print_info(f"Domain: {domain_name}")
            print_info(f"Status: {status}")
            
            return True, []
        else:
            print_warning(f"CloudFront distribution not found (optional component)")
            return True, []  # Not an error since it's optional
            
    except Exception as e:
        print_warning(f"Could not verify CloudFront: {str(e)}")
        return True, []  # Not an error since it's optional


def main():
    parser = argparse.ArgumentParser(
        description='Verify Voice for Bharat infrastructure setup',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--prefix',
        default='voice-for-bharat-dev',
        help='DynamoDB table prefix (default: voice-for-bharat-dev)'
    )
    
    parser.add_argument(
        '--environment',
        default='dev',
        help='Environment name (default: dev)'
    )
    
    parser.add_argument(
        '--skip-optional',
        action='store_true',
        help='Skip optional components (ElastiCache, CloudFront)'
    )
    
    args = parser.parse_args()
    
    print(f"\n{BLUE}Voice for Bharat - Infrastructure Verification{RESET}")
    print(f"{BLUE}Environment: {args.environment}{RESET}")
    print(f"{BLUE}Table Prefix: {args.prefix}{RESET}")
    
    all_results = []
    
    # Verify DynamoDB tables
    success, errors = verify_dynamodb_tables(args.prefix)
    all_results.append(('DynamoDB Tables', success, errors))
    
    # Verify S3 buckets
    success, errors = verify_s3_buckets(args.prefix, args.environment)
    all_results.append(('S3 Buckets', success, errors))
    
    # Verify Cognito User Pool
    success, errors = verify_cognito_user_pool(args.prefix, args.environment)
    all_results.append(('Cognito User Pool', success, errors))
    
    # Verify API Gateway
    success, errors = verify_api_gateway(args.prefix, args.environment)
    all_results.append(('API Gateway', success, errors))
    
    # Verify optional components
    if not args.skip_optional:
        success, errors = verify_elasticache(args.prefix, args.environment)
        all_results.append(('ElastiCache Redis', success, errors))
        
        success, errors = verify_cloudfront(args.environment)
        all_results.append(('CloudFront CDN', success, errors))
    
    # Print summary
    print_header("Verification Summary")
    
    passed = sum(1 for _, success, _ in all_results if success)
    total = len(all_results)
    
    for component, success, errors in all_results:
        if success:
            print_success(f"{component:30} - PASSED")
        else:
            print_error(f"{component:30} - FAILED")
            for error in errors:
                print_info(f"  • {error}")
    
    print(f"\n{BLUE}{'='*80}{RESET}")
    if passed == total:
        print(f"{GREEN}✓ All checks passed ({passed}/{total}){RESET}")
        print(f"\n{GREEN}Infrastructure is properly set up!{RESET}\n")
        sys.exit(0)
    else:
        print(f"{RED}✗ Some checks failed ({passed}/{total} passed){RESET}")
        print(f"\n{RED}Please review the errors above and fix the infrastructure issues.{RESET}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
