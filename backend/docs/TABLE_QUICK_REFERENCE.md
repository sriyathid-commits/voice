# DynamoDB Tables Quick Reference

Quick reference guide for Voice for Bharat DynamoDB tables. For detailed documentation, see [DYNAMODB_SCHEMAS.md](./DYNAMODB_SCHEMAS.md).

## Table Overview

| Table | Purpose | Primary Key | GSI Count | TTL |
|-------|---------|-------------|-----------|-----|
| users | User authentication & profile | userId | 3 | No |
| schemes | Government welfare schemes | schemeId | 3 | No |
| applications | User applications | applicationId | 3 | No |
| activity-log | User activity tracking | activityId | 3 | 90 days |
| user-profile | Extended profile data | userId | 2 | No |
| helplines | Support contact info | helplineId | 2 | No |
| guide-content | FAQ & guides | contentId | 3 | No |
| suggested-queries | Voice query suggestions | queryId | 3 | No |

## Quick Access Patterns

### Users Table

```python
# Get user by ID
table.get_item(Key={'userId': user_id})

# Login lookup by phone number
table.query(
    IndexName='phoneNumber-index',
    KeyConditionExpression='phoneNumber = :phone',
    ExpressionAttributeValues={':phone': '9876543210'}
)

# Users by state and category
table.query(
    IndexName='state-category-index',
    KeyConditionExpression='#state = :state AND category = :cat',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'MH', ':cat': 'OBC'}
)

# Cognito integration lookup
table.query(
    IndexName='cognitoId-index',
    KeyConditionExpression='cognitoId = :cid',
    ExpressionAttributeValues={':cid': cognito_id}
)
```

### Schemes Table

```python
# Get scheme by ID
table.get_item(Key={'schemeId': scheme_id})

# Schemes by state and category
table.query(
    IndexName='state-category-index',
    KeyConditionExpression='#state = :state AND category = :cat',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'KA', ':cat': 'agriculture'}
)

# Active schemes for sync
table.query(
    IndexName='isActive-lastSyncedAt-index',
    KeyConditionExpression='isActive = :active',
    ExpressionAttributeValues={':active': 'true'},
    ScanIndexForward=False  # Most recently synced first
)

# Popular schemes by category
table.query(
    IndexName='category-viewCount-index',
    KeyConditionExpression='category = :cat',
    ExpressionAttributeValues={':cat': 'health'},
    ScanIndexForward=False  # Highest view count first
)
```

### Applications Table

```python
# Get application by ID
table.get_item(Key={'applicationId': app_id})

# User's applications by status
table.query(
    IndexName='userId-status-index',
    KeyConditionExpression='userId = :uid AND #status = :status',
    ExpressionAttributeNames={'#status': 'status'},
    ExpressionAttributeValues={':uid': user_id, ':status': 'SUBMITTED'}
)

# All user's applications
table.query(
    IndexName='userId-status-index',
    KeyConditionExpression='userId = :uid',
    ExpressionAttributeValues={':uid': user_id}
)

# Applications by status (admin view)
table.query(
    IndexName='status-updatedAt-index',
    KeyConditionExpression='#status = :status',
    ExpressionAttributeNames={'#status': 'status'},
    ExpressionAttributeValues={':status': 'UNDER_REVIEW'},
    ScanIndexForward=False  # Most recently updated first
)

# Scheme applications (analytics)
table.query(
    IndexName='schemeId-submittedAt-index',
    KeyConditionExpression='schemeId = :sid',
    ExpressionAttributeValues={':sid': scheme_id},
    ScanIndexForward=False  # Most recent first
)
```

### Activity Log Table

```python
# User activity timeline
table.query(
    IndexName='userId-timestamp-index',
    KeyConditionExpression='userId = :uid',
    ExpressionAttributeValues={':uid': user_id},
    ScanIndexForward=False,  # Most recent first
    Limit=50
)

# Activity by type (analytics)
table.query(
    IndexName='type-timestamp-index',
    KeyConditionExpression='#type = :type',
    ExpressionAttributeNames={'#type': 'type'},
    ExpressionAttributeValues={':type': 'SCHEME_VIEWED'},
    ScanIndexForward=False
)

# Scheme-specific activity
table.query(
    IndexName='schemeId-timestamp-index',
    KeyConditionExpression='schemeId = :sid',
    ExpressionAttributeValues={':sid': scheme_id},
    ScanIndexForward=False
)

# Create activity with TTL (90 days)
import time
ttl = int(time.time()) + (90 * 24 * 60 * 60)
table.put_item(Item={
    'activityId': activity_id,
    'userId': user_id,
    'type': 'SCHEME_VIEWED',
    'timestamp': datetime.utcnow().isoformat(),
    'ttl': ttl,
    'metadata': {...}
})
```

### User Profile Table

```python
# Get profile by user ID
table.get_item(Key={'userId': user_id})

# Profiles by state (analytics)
table.query(
    IndexName='state-profileStrength-index',
    KeyConditionExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'TN'}
)

# Demographics query
table.query(
    IndexName='educationLevel-annualIncome-index',
    KeyConditionExpression='educationLevel = :edu AND annualIncome < :income',
    ExpressionAttributeValues={':edu': 'SECONDARY', ':income': 100000}
)
```

### Helplines Table

```python
# Get helpline by ID
table.get_item(Key={'helplineId': helpline_id})

# Helplines by state and category
table.query(
    IndexName='state-category-index',
    KeyConditionExpression='#state = :state AND category = :cat',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'AP', ':cat': 'health'}
)

# Active helplines by state
table.query(
    IndexName='isActive-state-index',
    KeyConditionExpression='isActive = :active AND #state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':active': 'true', ':state': 'GJ'}
)
```

### Guide Content Table

```python
# Get content by ID
table.get_item(Key={'contentId': content_id})

# Quick guides by priority
table.query(
    IndexName='category-state-priority-index',
    KeyConditionExpression='category = :cat',
    ExpressionAttributeValues={':cat': 'quick-guide'},
    ScanIndexForward=False,  # Highest priority first
    Limit=5
)

# Recent content updates
table.query(
    IndexName='state-lastUpdatedAt-index',
    KeyConditionExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'MH'},
    ScanIndexForward=False
)

# Popular content
table.query(
    IndexName='category-viewCount-index',
    KeyConditionExpression='category = :cat',
    ExpressionAttributeValues={':cat': 'faq'},
    ScanIndexForward=False
)
```

### Suggested Queries Table

```python
# Get query by ID
table.get_item(Key={'queryId': query_id})

# Display queries in order
table.query(
    IndexName='state-displayOrder-index',
    KeyConditionExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'KA'},
    ScanIndexForward=True,  # Ascending order
    Limit=3
)

# Popular queries by category
table.query(
    IndexName='category-popularity-index',
    KeyConditionExpression='category = :cat',
    ExpressionAttributeValues={':cat': 'ration-card'},
    ScanIndexForward=False
)

# Active queries by state
table.query(
    IndexName='isActive-state-index',
    KeyConditionExpression='isActive = :active AND #state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':active': 'true', ':state': 'ALL_INDIA'}
)
```

## Common Data Patterns

### Multilingual Content

```python
# Store multilingual data
item = {
    'schemeId': scheme_id,
    'name': {
        'en': 'PM-KISAN Scheme',
        'hi': 'पीएम-किसान योजना',
        'mr': 'पीएम-किसान योजना',
        'kn': 'ಪಿಎಂ-ಕಿಸಾನ್ ಯೋಜನೆ',
        'ta': 'பிஎம்-கிசான் திட்டம்',
        'te': 'పిఎం-కిసాన్ పథకం'
    }
}

# Retrieve in specific language
name_in_hindi = item['name'].get('hi', item['name']['en'])
```

### Timestamps

```python
from datetime import datetime, timezone

# Always use ISO 8601 format
timestamp = datetime.now(timezone.utc).isoformat()

# Store in item
item = {
    'userId': user_id,
    'createdAt': timestamp,
    'updatedAt': timestamp
}
```

### Status Tracking

```python
# Application status history
status_change = {
    'status': 'SUBMITTED',
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'reason': 'Application submitted successfully',
    'updatedBy': 'system'
}

# Append to status history
table.update_item(
    Key={'applicationId': app_id},
    UpdateExpression='SET #status = :status, updatedAt = :now, statusHistory = list_append(statusHistory, :change)',
    ExpressionAttributeNames={'#status': 'status'},
    ExpressionAttributeValues={
        ':status': 'SUBMITTED',
        ':now': datetime.now(timezone.utc).isoformat(),
        ':change': [status_change]
    }
)
```

### Encrypted Fields

```python
from cryptography.fernet import Fernet

# Encrypt sensitive data before storing
def encrypt_field(value: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(value.encode()).decode()

# Store encrypted
item = {
    'userId': user_id,
    'aadhaarNumber': encrypt_field(aadhaar, encryption_key),
    'panNumber': encrypt_field(pan, encryption_key)
}

# Decrypt when reading
def decrypt_field(encrypted_value: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(encrypted_value.encode()).decode()
```

## Environment Variables

```python
import os

# Table name construction
TABLE_PREFIX = os.getenv('DYNAMODB_TABLE_PREFIX', 'voice-for-bharat-dev')
USERS_TABLE = f"{TABLE_PREFIX}-users"
SCHEMES_TABLE = f"{TABLE_PREFIX}-schemes"
APPLICATIONS_TABLE = f"{TABLE_PREFIX}-applications"
ACTIVITY_LOG_TABLE = f"{TABLE_PREFIX}-activity-log"
USER_PROFILE_TABLE = f"{TABLE_PREFIX}-user-profile"
HELPLINES_TABLE = f"{TABLE_PREFIX}-helplines"
GUIDE_CONTENT_TABLE = f"{TABLE_PREFIX}-guide-content"
SUGGESTED_QUERIES_TABLE = f"{TABLE_PREFIX}-suggested-queries"
```

## Boto3 Setup

```python
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

# Get table reference
users_table = dynamodb.Table(USERS_TABLE)

# Initialize DynamoDB client (for admin operations)
dynamodb_client = boto3.client('dynamodb', region_name='ap-south-1')
```

## Error Handling

```python
from botocore.exceptions import ClientError

try:
    response = table.get_item(Key={'userId': user_id})
    item = response.get('Item')
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        print("Table not found")
    elif e.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
        print("Request rate too high")
    else:
        print(f"Unexpected error: {e}")
```

## Batch Operations

```python
# Batch get items
response = dynamodb_client.batch_get_item(
    RequestItems={
        USERS_TABLE: {
            'Keys': [
                {'userId': 'user1'},
                {'userId': 'user2'},
                {'userId': 'user3'}
            ]
        }
    }
)

# Batch write items
with table.batch_writer() as batch:
    for item in items:
        batch.put_item(Item=item)
```

## Pagination

```python
# Paginate through query results
response = table.query(
    IndexName='userId-timestamp-index',
    KeyConditionExpression='userId = :uid',
    ExpressionAttributeValues={':uid': user_id},
    Limit=20
)

items = response['Items']

# Get next page if available
while 'LastEvaluatedKey' in response:
    response = table.query(
        IndexName='userId-timestamp-index',
        KeyConditionExpression='userId = :uid',
        ExpressionAttributeValues={':uid': user_id},
        Limit=20,
        ExclusiveStartKey=response['LastEvaluatedKey']
    )
    items.extend(response['Items'])
```

## Conditional Updates

```python
# Update only if item exists
table.update_item(
    Key={'userId': user_id},
    UpdateExpression='SET profileStrength = :strength',
    ConditionExpression='attribute_exists(userId)',
    ExpressionAttributeValues={':strength': 85}
)

# Increment counter atomically
table.update_item(
    Key={'schemeId': scheme_id},
    UpdateExpression='SET viewCount = viewCount + :inc',
    ExpressionAttributeValues={':inc': 1}
)
```

## Testing Utilities

```python
# Check if table exists
def table_exists(table_name: str) -> bool:
    try:
        dynamodb_client.describe_table(TableName=table_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        raise

# Wait for table to be active
def wait_for_table(table_name: str):
    waiter = dynamodb_client.get_waiter('table_exists')
    waiter.wait(TableName=table_name)
```

## Performance Tips

1. **Use batch operations** for multiple items (up to 25 items per batch)
2. **Project only needed attributes** to reduce data transfer
3. **Use GSIs** instead of scans for queries
4. **Implement pagination** for large result sets
5. **Cache frequently accessed data** in ElastiCache
6. **Use consistent reads** only when necessary (costs 2x)
7. **Avoid hot partitions** by distributing writes evenly

## Common Mistakes to Avoid

❌ **Don't use Scan** - Use Query with GSI instead  
❌ **Don't store large items** - Keep items under 400KB  
❌ **Don't use reserved words** - Use ExpressionAttributeNames  
❌ **Don't forget TTL** - Set TTL for activity log items  
❌ **Don't hardcode table names** - Use environment variables  
❌ **Don't store unencrypted PII** - Encrypt sensitive fields  
❌ **Don't use boolean in GSI keys** - Use string "true"/"false"

## Monitoring Queries

```python
# CloudWatch metrics to monitor
metrics = [
    'ConsumedReadCapacityUnits',
    'ConsumedWriteCapacityUnits',
    'UserErrors',
    'SystemErrors',
    'ThrottledRequests'
]

# Get table metrics
cloudwatch = boto3.client('cloudwatch')
response = cloudwatch.get_metric_statistics(
    Namespace='AWS/DynamoDB',
    MetricName='ConsumedReadCapacityUnits',
    Dimensions=[{'Name': 'TableName', 'Value': USERS_TABLE}],
    StartTime=datetime.now() - timedelta(hours=1),
    EndTime=datetime.now(),
    Period=300,
    Statistics=['Sum']
)
```

## Additional Resources

- [Full Schema Documentation](./DYNAMODB_SCHEMAS.md)
- [Management Scripts](../scripts/README.md)
- [SAM Template](../template.yaml)
- [AWS DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/)
