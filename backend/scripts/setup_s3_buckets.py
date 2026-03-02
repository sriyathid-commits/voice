#!/usr/bin/env python3
"""
Script to set up and verify S3 bucket structure for Voice for Bharat.

This script:
1. Verifies S3 buckets exist
2. Checks encryption configuration
3. Verifies lifecycle policies
4. Checks CORS configuration
5. Creates placeholder files to establish folder structure
6. Tests presigned URL generation

Usage:
    python setup_s3_buckets.py --environment dev
    python setup_s3_buckets.py --environment production --verify-only
"""

import argparse
import boto3
import json
import sys
from botocore.exceptions import ClientError
from typing import Dict, List, Optional


class S3BucketSetup:
    """Setup and verify S3 buckets for Voice for Bharat"""
    
    def __init__(self, environment: str, region: str = "ap-south-1"):
        self.environment = environment
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.sts_client = boto3.client('sts', region_name=region)
        
        # Get AWS account ID
        self.account_id = self.sts_client.get_caller_identity()['Account']
        
        # Define bucket names
        self.buckets = {
            'documents': f'voice-for-bharat-documents-{environment}-{self.account_id}',
            'audio': f'voice-for-bharat-audio-{environment}-{self.account_id}',
            'scheme-dumps': f'voice-for-bharat-scheme-dumps-{environment}-{self.account_id}'
        }
        
        # Define folder structures
        self.folder_structures = {
            'documents': [
                'users/',
                'applications/'
            ],
            'audio': [
                'conversations/',
                'tts-cache/',
                'stt-recordings/'
            ],
            'scheme-dumps': [
                'daily/',
                'weekly/',
                'sources/'
            ]
        }
    
    def verify_bucket_exists(self, bucket_name: str) -> bool:
        """Check if bucket exists"""
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            print(f"✓ Bucket exists: {bucket_name}")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                print(f"✗ Bucket not found: {bucket_name}")
            else:
                print(f"✗ Error checking bucket {bucket_name}: {e}")
            return False
    
    def verify_encryption(self, bucket_name: str) -> bool:
        """Verify bucket encryption is enabled"""
        try:
            response = self.s3_client.get_bucket_encryption(Bucket=bucket_name)
            rules = response.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
            
            if rules:
                sse_algorithm = rules[0].get('ApplyServerSideEncryptionByDefault', {}).get('SSEAlgorithm')
                if sse_algorithm == 'AES256':
                    print(f"  ✓ Encryption enabled (SSE-S3): {bucket_name}")
                    return True
                else:
                    print(f"  ⚠ Unexpected encryption algorithm: {sse_algorithm}")
                    return False
            else:
                print(f"  ✗ No encryption rules found: {bucket_name}")
                return False
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                print(f"  ✗ Encryption not configured: {bucket_name}")
            else:
                print(f"  ✗ Error checking encryption: {e}")
            return False
    
    def verify_lifecycle_policies(self, bucket_name: str, bucket_type: str) -> bool:
        """Verify lifecycle policies are configured"""
        try:
            response = self.s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            rules = response.get('Rules', [])
            
            if not rules:
                print(f"  ✗ No lifecycle rules found: {bucket_name}")
                return False
            
            print(f"  ✓ Lifecycle policies configured: {bucket_name}")
            for rule in rules:
                rule_id = rule.get('ID', 'Unknown')
                status = rule.get('Status', 'Unknown')
                print(f"    - {rule_id}: {status}")
            
            # Verify specific rules based on bucket type
            if bucket_type == 'documents':
                expected_rules = ['TransitionToIA', 'TransitionToGlacier', 'DeleteAfter7Years']
            elif bucket_type == 'audio':
                expected_rules = ['DeleteConversationsAfter30Days', 'DeleteTTSCacheAfter90Days', 'DeleteSTTRecordingsAfter7Days']
            elif bucket_type == 'scheme-dumps':
                expected_rules = ['DeleteDailyDumpsAfter30Days', 'DeleteWeeklyDumpsAfter1Year', 'ArchiveSourceDataToGlacier']
            else:
                return True
            
            rule_ids = [rule.get('ID') for rule in rules]
            missing_rules = [rule for rule in expected_rules if rule not in rule_ids]
            
            if missing_rules:
                print(f"  ⚠ Missing expected rules: {', '.join(missing_rules)}")
                return False
            
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                print(f"  ✗ No lifecycle configuration: {bucket_name}")
            else:
                print(f"  ✗ Error checking lifecycle: {e}")
            return False
    
    def verify_cors(self, bucket_name: str) -> bool:
        """Verify CORS configuration"""
        try:
            response = self.s3_client.get_bucket_cors(Bucket=bucket_name)
            cors_rules = response.get('CORSRules', [])
            
            if cors_rules:
                print(f"  ✓ CORS configured: {bucket_name}")
                for i, rule in enumerate(cors_rules):
                    allowed_methods = rule.get('AllowedMethods', [])
                    allowed_origins = rule.get('AllowedOrigins', [])
                    print(f"    - Rule {i+1}: Methods={allowed_methods}, Origins={allowed_origins}")
                return True
            else:
                print(f"  ✗ No CORS rules found: {bucket_name}")
                return False
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchCORSConfiguration':
                print(f"  ✗ CORS not configured: {bucket_name}")
            else:
                print(f"  ✗ Error checking CORS: {e}")
            return False
    
    def verify_versioning(self, bucket_name: str, bucket_type: str) -> bool:
        """Verify versioning configuration"""
        try:
            response = self.s3_client.get_bucket_versioning(Bucket=bucket_name)
            status = response.get('Status', 'Disabled')
            
            # Versioning should be enabled for documents and scheme-dumps
            if bucket_type in ['documents', 'scheme-dumps']:
                if status == 'Enabled':
                    print(f"  ✓ Versioning enabled: {bucket_name}")
                    return True
                else:
                    print(f"  ✗ Versioning not enabled: {bucket_name} (Status: {status})")
                    return False
            else:
                print(f"  ℹ Versioning not required: {bucket_name}")
                return True
        except ClientError as e:
            print(f"  ✗ Error checking versioning: {e}")
            return False
    
    def create_folder_structure(self, bucket_name: str, bucket_type: str) -> bool:
        """Create folder structure by uploading placeholder files"""
        try:
            folders = self.folder_structures.get(bucket_type, [])
            
            for folder in folders:
                # Create a placeholder file to establish the folder
                key = f"{folder}.placeholder"
                self.s3_client.put_object(
                    Bucket=bucket_name,
                    Key=key,
                    Body=b'',
                    Metadata={'purpose': 'folder-structure'}
                )
            
            print(f"  ✓ Folder structure created: {bucket_name}")
            print(f"    Folders: {', '.join(folders)}")
            return True
        except ClientError as e:
            print(f"  ✗ Error creating folder structure: {e}")
            return False
    
    def test_presigned_url(self, bucket_name: str) -> bool:
        """Test presigned URL generation"""
        try:
            # Create a test object
            test_key = 'test/presigned-url-test.txt'
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=test_key,
                Body=b'Test content for presigned URL'
            )
            
            # Generate presigned URL
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': test_key},
                ExpiresIn=900  # 15 minutes
            )
            
            if url:
                print(f"  ✓ Presigned URL generation works: {bucket_name}")
                print(f"    URL: {url[:80]}...")
                
                # Clean up test object
                self.s3_client.delete_object(Bucket=bucket_name, Key=test_key)
                return True
            else:
                print(f"  ✗ Failed to generate presigned URL: {bucket_name}")
                return False
        except ClientError as e:
            print(f"  ✗ Error testing presigned URL: {e}")
            return False
    
    def verify_all_buckets(self) -> Dict[str, bool]:
        """Verify all buckets and their configurations"""
        results = {}
        
        print("\n" + "="*80)
        print("S3 BUCKET VERIFICATION")
        print("="*80)
        print(f"Environment: {self.environment}")
        print(f"Region: {self.region}")
        print(f"Account ID: {self.account_id}")
        print("="*80 + "\n")
        
        for bucket_type, bucket_name in self.buckets.items():
            print(f"\n📦 Checking {bucket_type.upper()} bucket: {bucket_name}")
            print("-" * 80)
            
            checks = {
                'exists': self.verify_bucket_exists(bucket_name),
                'encryption': False,
                'lifecycle': False,
                'cors': False,
                'versioning': False
            }
            
            if checks['exists']:
                checks['encryption'] = self.verify_encryption(bucket_name)
                checks['lifecycle'] = self.verify_lifecycle_policies(bucket_name, bucket_type)
                checks['cors'] = self.verify_cors(bucket_name)
                checks['versioning'] = self.verify_versioning(bucket_name, bucket_type)
            
            results[bucket_type] = all(checks.values())
            
            if results[bucket_type]:
                print(f"\n✓ All checks passed for {bucket_type} bucket")
            else:
                print(f"\n✗ Some checks failed for {bucket_type} bucket")
        
        return results
    
    def setup_all_buckets(self) -> Dict[str, bool]:
        """Set up folder structure in all buckets"""
        results = {}
        
        print("\n" + "="*80)
        print("S3 BUCKET SETUP")
        print("="*80)
        print(f"Environment: {self.environment}")
        print(f"Region: {self.region}")
        print("="*80 + "\n")
        
        for bucket_type, bucket_name in self.buckets.items():
            print(f"\n📦 Setting up {bucket_type.upper()} bucket: {bucket_name}")
            print("-" * 80)
            
            if not self.verify_bucket_exists(bucket_name):
                print(f"  ✗ Bucket does not exist. Please deploy CloudFormation stack first.")
                results[bucket_type] = False
                continue
            
            # Create folder structure
            folder_result = self.create_folder_structure(bucket_name, bucket_type)
            
            # Test presigned URL generation
            presigned_result = self.test_presigned_url(bucket_name)
            
            results[bucket_type] = folder_result and presigned_result
        
        return results
    
    def print_summary(self, results: Dict[str, bool]):
        """Print summary of results"""
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        all_passed = all(results.values())
        
        for bucket_type, passed in results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{status}: {bucket_type} bucket")
        
        print("="*80)
        
        if all_passed:
            print("\n✓ All buckets are properly configured!")
            return 0
        else:
            print("\n✗ Some buckets have issues. Please review the output above.")
            return 1


def main():
    parser = argparse.ArgumentParser(
        description='Set up and verify S3 buckets for Voice for Bharat'
    )
    parser.add_argument(
        '--environment',
        type=str,
        required=True,
        choices=['dev', 'staging', 'production'],
        help='Deployment environment'
    )
    parser.add_argument(
        '--region',
        type=str,
        default='ap-south-1',
        help='AWS region (default: ap-south-1)'
    )
    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Only verify configuration, do not create folder structure'
    )
    
    args = parser.parse_args()
    
    setup = S3BucketSetup(args.environment, args.region)
    
    if args.verify_only:
        results = setup.verify_all_buckets()
    else:
        # First verify, then setup
        verify_results = setup.verify_all_buckets()
        if all(verify_results.values()):
            results = setup.setup_all_buckets()
        else:
            print("\n⚠ Verification failed. Please fix issues before setting up folder structure.")
            results = verify_results
    
    exit_code = setup.print_summary(results)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
