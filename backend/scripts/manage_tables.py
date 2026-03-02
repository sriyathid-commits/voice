#!/usr/bin/env python3
"""
DynamoDB Table Management Script

This script provides utilities for managing DynamoDB tables including:
- Listing all tables
- Describing table schemas
- Checking table status
- Validating table configuration
- Generating sample data

Usage:
    python manage_tables.py list
    python manage_tables.py describe users
    python manage_tables.py validate
    python manage_tables.py status
"""

import argparse
import boto3
import json
import sys
from typing import Dict, List, Optional
from datetime import datetime, timezone


# Table prefix from environment or default
TABLE_PREFIX = "voice-for-bharat-dev"

# Expected tables
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


def get_dynamodb_client():
    """Get DynamoDB client"""
    return boto3.client('dynamodb')


def get_dynamodb_resource():
    """Get DynamoDB resource"""
    return boto3.resource('dynamodb')


def list_tables(prefix: str = TABLE_PREFIX) -> List[str]:
    """List all tables with the given prefix"""
    client = get_dynamodb_client()
    
    try:
        response = client.list_tables()
        all_tables = response.get('TableNames', [])
        
        # Filter tables by prefix
        filtered_tables = [t for t in all_tables if t.startswith(prefix)]
        
        return filtered_tables
    except Exception as e:
        print(f"Error listing tables: {e}")
        return []


def describe_table(table_name: str) -> Optional[Dict]:
    """Describe a DynamoDB table"""
    client = get_dynamodb_client()
    
    try:
        response = client.describe_table(TableName=table_name)
        return response.get('Table')
    except client.exceptions.ResourceNotFoundException:
        print(f"Table {table_name} not found")
        return None
    except Exception as e:
        print(f"Error describing table {table_name}: {e}")
        return None


def get_table_status(table_name: str) -> str:
    """Get the status of a table"""
    table_info = describe_table(table_name)
    if table_info:
        return table_info.get('TableStatus', 'UNKNOWN')
    return 'NOT_FOUND'


def validate_table_configuration(table_name: str) -> Dict[str, bool]:
    """Validate table configuration against requirements"""
    table_info = describe_table(table_name)
    
    if not table_info:
        return {'exists': False}
    
    validation = {
        'exists': True,
        'billing_mode': table_info.get('BillingModeSummary', {}).get('BillingMode') == 'PAY_PER_REQUEST',
        'encryption': table_info.get('SSEDescription', {}).get('Status') == 'ENABLED',
        'pitr': False,  # Need to check separately
        'status': table_info.get('TableStatus') == 'ACTIVE'
    }
    
    # Check Point-in-Time Recovery
    client = get_dynamodb_client()
    try:
        pitr_response = client.describe_continuous_backups(TableName=table_name)
        pitr_status = pitr_response.get('ContinuousBackupsDescription', {}).get('PointInTimeRecoveryDescription', {}).get('PointInTimeRecoveryStatus')
        validation['pitr'] = pitr_status == 'ENABLED'
    except Exception:
        validation['pitr'] = False
    
    return validation


def print_table_info(table_name: str):
    """Print detailed table information"""
    table_info = describe_table(table_name)
    
    if not table_info:
        print(f"Table {table_name} not found")
        return
    
    print(f"\n{'='*80}")
    print(f"Table: {table_name}")
    print(f"{'='*80}")
    
    print(f"\nStatus: {table_info.get('TableStatus')}")
    print(f"Creation Date: {table_info.get('CreationDateTime')}")
    print(f"Item Count: {table_info.get('ItemCount', 0):,}")
    print(f"Table Size: {table_info.get('TableSizeBytes', 0):,} bytes")
    
    # Billing mode
    billing_mode = table_info.get('BillingModeSummary', {}).get('BillingMode', 'PROVISIONED')
    print(f"\nBilling Mode: {billing_mode}")
    
    # Key schema
    print("\nKey Schema:")
    for key in table_info.get('KeySchema', []):
        key_type = 'Partition Key' if key['KeyType'] == 'HASH' else 'Sort Key'
        print(f"  - {key['AttributeName']} ({key_type})")
    
    # Attribute definitions
    print("\nAttribute Definitions:")
    for attr in table_info.get('AttributeDefinitions', []):
        attr_type = {'S': 'String', 'N': 'Number', 'B': 'Binary'}.get(attr['AttributeType'], attr['AttributeType'])
        print(f"  - {attr['AttributeName']}: {attr_type}")
    
    # Global Secondary Indexes
    gsi_list = table_info.get('GlobalSecondaryIndexes', [])
    if gsi_list:
        print(f"\nGlobal Secondary Indexes ({len(gsi_list)}):")
        for gsi in gsi_list:
            print(f"  - {gsi['IndexName']}")
            print(f"    Status: {gsi.get('IndexStatus')}")
            print(f"    Keys: ", end='')
            keys = []
            for key in gsi.get('KeySchema', []):
                key_type = 'PK' if key['KeyType'] == 'HASH' else 'SK'
                keys.append(f"{key['AttributeName']} ({key_type})")
            print(', '.join(keys))
            print(f"    Projection: {gsi.get('Projection', {}).get('ProjectionType')}")
    
    # TTL
    client = get_dynamodb_client()
    try:
        ttl_response = client.describe_time_to_live(TableName=table_name)
        ttl_status = ttl_response.get('TimeToLiveDescription', {}).get('TimeToLiveStatus')
        if ttl_status == 'ENABLED':
            ttl_attr = ttl_response.get('TimeToLiveDescription', {}).get('AttributeName')
            print(f"\nTTL: Enabled (attribute: {ttl_attr})")
        else:
            print(f"\nTTL: Disabled")
    except Exception:
        print("\nTTL: Unknown")
    
    # Encryption
    sse = table_info.get('SSEDescription', {})
    if sse:
        print(f"\nEncryption: {sse.get('Status', 'DISABLED')}")
        if sse.get('SSEType'):
            print(f"  Type: {sse.get('SSEType')}")
    
    # Point-in-Time Recovery
    try:
        pitr_response = client.describe_continuous_backups(TableName=table_name)
        pitr_status = pitr_response.get('ContinuousBackupsDescription', {}).get('PointInTimeRecoveryDescription', {}).get('PointInTimeRecoveryStatus')
        print(f"\nPoint-in-Time Recovery: {pitr_status}")
    except Exception:
        print("\nPoint-in-Time Recovery: Unknown")
    
    # Tags
    try:
        tags_response = client.list_tags_of_resource(ResourceArn=table_info['TableArn'])
        tags = tags_response.get('Tags', [])
        if tags:
            print("\nTags:")
            for tag in tags:
                print(f"  - {tag['Key']}: {tag['Value']}")
    except Exception:
        pass


def validate_all_tables():
    """Validate all expected tables"""
    print(f"\nValidating DynamoDB Tables (Prefix: {TABLE_PREFIX})")
    print(f"{'='*80}\n")
    
    results = []
    
    for table_short_name in EXPECTED_TABLES:
        table_name = f"{TABLE_PREFIX}-{table_short_name}"
        validation = validate_table_configuration(table_name)
        
        status_icon = "✓" if validation.get('exists') else "✗"
        print(f"{status_icon} {table_short_name:20} ", end='')
        
        if validation.get('exists'):
            checks = []
            checks.append("✓ Active" if validation.get('status') else "✗ Not Active")
            checks.append("✓ On-Demand" if validation.get('billing_mode') else "✗ Provisioned")
            checks.append("✓ Encrypted" if validation.get('encryption') else "✗ Not Encrypted")
            checks.append("✓ PITR" if validation.get('pitr') else "✗ No PITR")
            print(" | ".join(checks))
        else:
            print("NOT FOUND")
        
        results.append({
            'table': table_short_name,
            'validation': validation
        })
    
    # Summary
    print(f"\n{'='*80}")
    existing_count = sum(1 for r in results if r['validation'].get('exists'))
    print(f"Summary: {existing_count}/{len(EXPECTED_TABLES)} tables found")
    
    if existing_count < len(EXPECTED_TABLES):
        print("\nMissing tables:")
        for r in results:
            if not r['validation'].get('exists'):
                print(f"  - {r['table']}")
    
    return results


def check_table_status():
    """Check status of all tables"""
    print(f"\nTable Status (Prefix: {TABLE_PREFIX})")
    print(f"{'='*80}\n")
    
    tables = list_tables(TABLE_PREFIX)
    
    if not tables:
        print("No tables found with the specified prefix")
        return
    
    print(f"{'Table Name':<50} {'Status':<15} {'Items':<15}")
    print(f"{'-'*80}")
    
    for table_name in sorted(tables):
        table_info = describe_table(table_name)
        if table_info:
            status = table_info.get('TableStatus', 'UNKNOWN')
            item_count = table_info.get('ItemCount', 0)
            print(f"{table_name:<50} {status:<15} {item_count:>14,}")
        else:
            print(f"{table_name:<50} {'ERROR':<15} {'-':>14}")


def generate_sample_data():
    """Generate sample data for testing"""
    print("\nGenerating sample data...")
    print("This feature is not yet implemented.")
    print("Use the seed_data.py script to populate tables with sample data.")


def main():
    parser = argparse.ArgumentParser(
        description='DynamoDB Table Management Utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_tables.py list
  python manage_tables.py describe users
  python manage_tables.py validate
  python manage_tables.py status
        """
    )
    
    parser.add_argument(
        'command',
        choices=['list', 'describe', 'validate', 'status', 'sample'],
        help='Command to execute'
    )
    
    parser.add_argument(
        'table',
        nargs='?',
        help='Table name (short name without prefix) for describe command'
    )
    
    parser.add_argument(
        '--prefix',
        default=TABLE_PREFIX,
        help=f'Table name prefix (default: {TABLE_PREFIX})'
    )
    
    args = parser.parse_args()
    
    # Update global prefix if provided
    global TABLE_PREFIX
    TABLE_PREFIX = args.prefix
    
    if args.command == 'list':
        tables = list_tables(TABLE_PREFIX)
        print(f"\nTables with prefix '{TABLE_PREFIX}':")
        for table in sorted(tables):
            print(f"  - {table}")
        print(f"\nTotal: {len(tables)} tables")
    
    elif args.command == 'describe':
        if not args.table:
            print("Error: table name required for describe command")
            sys.exit(1)
        
        table_name = f"{TABLE_PREFIX}-{args.table}" if not args.table.startswith(TABLE_PREFIX) else args.table
        print_table_info(table_name)
    
    elif args.command == 'validate':
        validate_all_tables()
    
    elif args.command == 'status':
        check_table_status()
    
    elif args.command == 'sample':
        generate_sample_data()


if __name__ == '__main__':
    main()
