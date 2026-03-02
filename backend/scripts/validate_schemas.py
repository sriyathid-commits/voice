#!/usr/bin/env python3
"""
DynamoDB Schema Validation Script

Validates that deployed DynamoDB tables match the expected schema definitions.
This script checks:
- Table existence
- Key schema (partition key, sort key)
- Global Secondary Indexes
- Attribute definitions
- TTL configuration
- Billing mode
- Encryption settings
- Point-in-Time Recovery

Usage:
    python validate_schemas.py
    python validate_schemas.py --table users
    python validate_schemas.py --prefix voice-for-bharat-prod
"""

import argparse
import boto3
import sys
from typing import Dict, List, Optional, Tuple


# Expected schema definitions
EXPECTED_SCHEMAS = {
    "users": {
        "partition_key": ("userId", "S"),
        "sort_key": None,
        "gsi": [
            {
                "name": "phoneNumber-index",
                "partition_key": ("phoneNumber", "S"),
                "sort_key": None
            },
            {
                "name": "state-category-index",
                "partition_key": ("state", "S"),
                "sort_key": ("category", "S")
            },
            {
                "name": "cognitoId-index",
                "partition_key": ("cognitoId", "S"),
                "sort_key": None
            }
        ],
        "ttl": None
    },
    "schemes": {
        "partition_key": ("schemeId", "S"),
        "sort_key": None,
        "gsi": [
            {
                "name": "state-category-index",
                "partition_key": ("state", "S"),
                "sort_key": ("category", "S")
            },
            {
                "name": "isActive-lastSyncedAt-index",
                "partition_key": ("isActive", "S"),
                "sort_key": ("lastSyncedAt", "S")
            },
            {
                "name": "category-viewCount-index",
                "partition_key": ("category", "S"),
                "sort_key": ("viewCount", "N")
            }
        ],
        "ttl": None
    },
    "applications": {
        "partition_key": ("applicationId", "S"),
        "sort_key": None,
        "gsi": [
            {
                "name": "userId-status-index",
                "partition_key": ("userId", "S"),
                "sort_key": ("status", "S")
            },
            {
                "name": "schemeId-submittedAt-index",
                "partition_key": ("schemeId", "S"),
                "sort_key": ("submittedAt", "S")
            },
            {
                "name": "status-updatedAt-index",
                "partition_key": ("status", "S"),
                "sort_key": ("updatedAt", "S")
            }
        ],
        "ttl": None
    },
    "activity-log": {
        "partition_key": ("activityId", "S"),
        "sort_key": None,
        "gsi": [
            {
                "name": "userId-timestamp-index",
                "partition_key": ("userId", "S"),
                "sort_key": ("timestamp", "S")
            },
            {
                "name": "type-timestamp-index",
                "partition_key": ("type", "S"),
                "sort_key": ("timestamp", "S")
            },
            {
                "name": "schemeId-timestamp-index",
                "partition_key": ("schemeId", "S"),
                "sort_key": ("timestamp", "S")
            }
        ],
        "ttl": "ttl"
    },
    "user-profile": {
        "partition_key": ("userId", "S"),
        "sort_key": None,
        "gsi": [
            {
                "name": "state-profileStrength-index",
                "partition_key": ("state", "S"),
                "sort_key": ("profileStrength", "N")
            },
            {
                "name": "educationLevel-annualIncome-index",
                "partition_key": ("educationLevel", "S"),
                "sort_key": ("annualIncome", "N")
            }
        ],
        "ttl": None
    },
    "helplines": {
        "partition_key": ("helplineId", "S"),
        "sort_key": None,
        "gsi": [
            {
                "name": "state-category-index",
                "partition_key": ("state", "S"),
                "sort_key": ("category", "S")
            },
            {
                "name": "isActive-state-index",
                "partition_key": ("isActive", "S"),
                "sort_key": ("state", "S")
            }
        ],
        "ttl": None
    },
    "guide-content": {
        "partition_key": ("contentId", "S"),
        "sort_key": None,
        "gsi": [
            {
                "name": "category-state-priority-index",
                "partition_key": ("category", "S"),
                "sort_key": ("priority", "N")
            },
            {
                "name": "state-lastUpdatedAt-index",
                "partition_key": ("state", "S"),
                "sort_key": ("lastUpdatedAt", "S")
            },
            {
                "name": "category-viewCount-index",
                "partition_key": ("category", "S"),
                "sort_key": ("viewCount", "N")
            }
        ],
        "ttl": None
    },
    "suggested-queries": {
        "partition_key": ("queryId", "S"),
        "sort_key": None,
        "gsi": [
            {
                "name": "state-displayOrder-index",
                "partition_key": ("state", "S"),
                "sort_key": ("displayOrder", "N")
            },
            {
                "name": "category-popularity-index",
                "partition_key": ("category", "S"),
                "sort_key": ("popularity", "N")
            },
            {
                "name": "isActive-state-index",
                "partition_key": ("isActive", "S"),
                "sort_key": ("state", "S")
            }
        ],
        "ttl": None
    }
}


def get_dynamodb_client():
    """Get DynamoDB client"""
    return boto3.client('dynamodb')


def get_table_schema(table_name: str) -> Optional[Dict]:
    """Get actual table schema from DynamoDB"""
    client = get_dynamodb_client()
    
    try:
        response = client.describe_table(TableName=table_name)
        return response.get('Table')
    except client.exceptions.ResourceNotFoundException:
        return None
    except Exception as e:
        print(f"Error getting table schema: {e}")
        return None


def validate_key_schema(table_name: str, expected: Dict, actual: Dict) -> Tuple[bool, List[str]]:
    """Validate table key schema"""
    errors = []
    
    # Get actual key schema
    actual_keys = {key['AttributeName']: key['KeyType'] for key in actual.get('KeySchema', [])}
    actual_attrs = {attr['AttributeName']: attr['AttributeType'] for attr in actual.get('AttributeDefinitions', [])}
    
    # Validate partition key
    pk_name, pk_type = expected['partition_key']
    if pk_name not in actual_keys:
        errors.append(f"Missing partition key: {pk_name}")
    elif actual_keys[pk_name] != 'HASH':
        errors.append(f"Partition key {pk_name} has wrong key type: {actual_keys[pk_name]}")
    elif actual_attrs.get(pk_name) != pk_type:
        errors.append(f"Partition key {pk_name} has wrong attribute type: {actual_attrs.get(pk_name)} (expected {pk_type})")
    
    # Validate sort key
    if expected['sort_key']:
        sk_name, sk_type = expected['sort_key']
        if sk_name not in actual_keys:
            errors.append(f"Missing sort key: {sk_name}")
        elif actual_keys[sk_name] != 'RANGE':
            errors.append(f"Sort key {sk_name} has wrong key type: {actual_keys[sk_name]}")
        elif actual_attrs.get(sk_name) != sk_type:
            errors.append(f"Sort key {sk_name} has wrong attribute type: {actual_attrs.get(sk_name)} (expected {sk_type})")
    
    return len(errors) == 0, errors


def validate_gsi(table_name: str, expected: Dict, actual: Dict) -> Tuple[bool, List[str]]:
    """Validate Global Secondary Indexes"""
    errors = []
    
    expected_gsi = expected.get('gsi', [])
    actual_gsi = actual.get('GlobalSecondaryIndexes', [])
    
    # Check GSI count
    if len(expected_gsi) != len(actual_gsi):
        errors.append(f"GSI count mismatch: expected {len(expected_gsi)}, found {len(actual_gsi)}")
    
    # Build lookup for actual GSI
    actual_gsi_map = {gsi['IndexName']: gsi for gsi in actual_gsi}
    actual_attrs = {attr['AttributeName']: attr['AttributeType'] for attr in actual.get('AttributeDefinitions', [])}
    
    # Validate each expected GSI
    for exp_gsi in expected_gsi:
        gsi_name = exp_gsi['name']
        
        if gsi_name not in actual_gsi_map:
            errors.append(f"Missing GSI: {gsi_name}")
            continue
        
        act_gsi = actual_gsi_map[gsi_name]
        act_keys = {key['AttributeName']: key['KeyType'] for key in act_gsi.get('KeySchema', [])}
        
        # Validate GSI partition key
        pk_name, pk_type = exp_gsi['partition_key']
        if pk_name not in act_keys:
            errors.append(f"GSI {gsi_name}: Missing partition key {pk_name}")
        elif act_keys[pk_name] != 'HASH':
            errors.append(f"GSI {gsi_name}: Partition key {pk_name} has wrong key type")
        elif actual_attrs.get(pk_name) != pk_type:
            errors.append(f"GSI {gsi_name}: Partition key {pk_name} has wrong attribute type: {actual_attrs.get(pk_name)} (expected {pk_type})")
        
        # Validate GSI sort key
        if exp_gsi['sort_key']:
            sk_name, sk_type = exp_gsi['sort_key']
            if sk_name not in act_keys:
                errors.append(f"GSI {gsi_name}: Missing sort key {sk_name}")
            elif act_keys[sk_name] != 'RANGE':
                errors.append(f"GSI {gsi_name}: Sort key {sk_name} has wrong key type")
            elif actual_attrs.get(sk_name) != sk_type:
                errors.append(f"GSI {gsi_name}: Sort key {sk_name} has wrong attribute type: {actual_attrs.get(sk_name)} (expected {sk_type})")
    
    return len(errors) == 0, errors


def validate_ttl(table_name: str, expected: Dict) -> Tuple[bool, List[str]]:
    """Validate TTL configuration"""
    errors = []
    client = get_dynamodb_client()
    
    expected_ttl = expected.get('ttl')
    
    try:
        response = client.describe_time_to_live(TableName=table_name)
        ttl_desc = response.get('TimeToLiveDescription', {})
        ttl_status = ttl_desc.get('TimeToLiveStatus')
        ttl_attr = ttl_desc.get('AttributeName')
        
        if expected_ttl:
            if ttl_status != 'ENABLED':
                errors.append(f"TTL should be enabled but is {ttl_status}")
            elif ttl_attr != expected_ttl:
                errors.append(f"TTL attribute should be {expected_ttl} but is {ttl_attr}")
        else:
            if ttl_status == 'ENABLED':
                errors.append(f"TTL should not be enabled but is enabled on {ttl_attr}")
    except Exception as e:
        errors.append(f"Error checking TTL: {e}")
    
    return len(errors) == 0, errors


def validate_configuration(table_name: str, actual: Dict) -> Tuple[bool, List[str]]:
    """Validate table configuration (billing, encryption, PITR)"""
    errors = []
    client = get_dynamodb_client()
    
    # Check billing mode
    billing_mode = actual.get('BillingModeSummary', {}).get('BillingMode')
    if billing_mode != 'PAY_PER_REQUEST':
        errors.append(f"Billing mode should be PAY_PER_REQUEST but is {billing_mode}")
    
    # Check encryption
    sse = actual.get('SSEDescription', {})
    if sse.get('Status') != 'ENABLED':
        errors.append("Encryption should be enabled")
    
    # Check Point-in-Time Recovery
    try:
        pitr_response = client.describe_continuous_backups(TableName=table_name)
        pitr_status = pitr_response.get('ContinuousBackupsDescription', {}).get('PointInTimeRecoveryDescription', {}).get('PointInTimeRecoveryStatus')
        if pitr_status != 'ENABLED':
            errors.append(f"Point-in-Time Recovery should be enabled but is {pitr_status}")
    except Exception as e:
        errors.append(f"Error checking PITR: {e}")
    
    return len(errors) == 0, errors


def validate_table(table_short_name: str, prefix: str) -> Tuple[bool, List[str]]:
    """Validate a single table"""
    table_name = f"{prefix}-{table_short_name}"
    expected = EXPECTED_SCHEMAS.get(table_short_name)
    
    if not expected:
        return False, [f"No expected schema defined for {table_short_name}"]
    
    # Get actual schema
    actual = get_table_schema(table_name)
    if not actual:
        return False, [f"Table {table_name} not found"]
    
    all_errors = []
    
    # Validate key schema
    valid, errors = validate_key_schema(table_name, expected, actual)
    all_errors.extend(errors)
    
    # Validate GSI
    valid, errors = validate_gsi(table_name, expected, actual)
    all_errors.extend(errors)
    
    # Validate TTL
    valid, errors = validate_ttl(table_name, expected)
    all_errors.extend(errors)
    
    # Validate configuration
    valid, errors = validate_configuration(table_name, actual)
    all_errors.extend(errors)
    
    return len(all_errors) == 0, all_errors


def main():
    parser = argparse.ArgumentParser(
        description='Validate DynamoDB table schemas',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--table',
        help='Validate specific table (short name without prefix)'
    )
    
    parser.add_argument(
        '--prefix',
        default='voice-for-bharat-dev',
        help='Table name prefix (default: voice-for-bharat-dev)'
    )
    
    args = parser.parse_args()
    
    print(f"\nValidating DynamoDB Schemas (Prefix: {args.prefix})")
    print(f"{'='*80}\n")
    
    tables_to_validate = [args.table] if args.table else list(EXPECTED_SCHEMAS.keys())
    
    results = []
    for table_short_name in tables_to_validate:
        print(f"Validating {table_short_name}...", end=' ')
        
        valid, errors = validate_table(table_short_name, args.prefix)
        
        if valid:
            print("✓ PASS")
        else:
            print("✗ FAIL")
            for error in errors:
                print(f"  - {error}")
        
        results.append({
            'table': table_short_name,
            'valid': valid,
            'errors': errors
        })
        print()
    
    # Summary
    print(f"{'='*80}")
    passed = sum(1 for r in results if r['valid'])
    total = len(results)
    print(f"Summary: {passed}/{total} tables passed validation")
    
    if passed < total:
        print("\nFailed tables:")
        for r in results:
            if not r['valid']:
                print(f"  - {r['table']} ({len(r['errors'])} errors)")
        sys.exit(1)
    else:
        print("\n✓ All tables passed validation!")
        sys.exit(0)


if __name__ == '__main__':
    main()
