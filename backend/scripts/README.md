# DynamoDB Table Management Scripts

This directory contains utility scripts for managing and validating DynamoDB tables for the Voice for Bharat application.

## Prerequisites

```bash
# Install required dependencies
pip install boto3

# Configure AWS credentials
aws configure
```

## Scripts

### 1. manage_tables.py

Comprehensive table management utility for listing, describing, and checking table status.

**Usage:**

```bash
# List all tables with the default prefix
python manage_tables.py list

# List tables with custom prefix
python manage_tables.py list --prefix voice-for-bharat-prod

# Describe a specific table (detailed information)
python manage_tables.py describe users
python manage_tables.py describe schemes --prefix voice-for-bharat-prod

# Validate all tables (check configuration)
python manage_tables.py validate

# Check status of all tables
python manage_tables.py status
```

**Features:**
- List all tables with a given prefix
- Describe table schema, indexes, and configuration
- Validate table configuration (billing mode, encryption, PITR)
- Check table status and item counts
- Display GSI information
- Show TTL configuration

**Example Output:**

```
Table: voice-for-bharat-dev-users
================================================================================

Status: ACTIVE
Creation Date: 2024-01-15 10:30:00
Item Count: 1,234
Table Size: 524,288 bytes

Billing Mode: PAY_PER_REQUEST

Key Schema:
  - userId (Partition Key)

Attribute Definitions:
  - userId: String
  - phoneNumber: String
  - state: String
  - category: String
  - cognitoId: String

Global Secondary Indexes (3):
  - phoneNumber-index
    Status: ACTIVE
    Keys: phoneNumber (PK)
    Projection: ALL
  - state-category-index
    Status: ACTIVE
    Keys: state (PK), category (SK)
    Projection: ALL
  - cognitoId-index
    Status: ACTIVE
    Keys: cognitoId (PK)
    Projection: ALL

TTL: Disabled

Encryption: ENABLED
  Type: KMS

Point-in-Time Recovery: ENABLED
```

---

### 2. validate_schemas.py

Validates that deployed DynamoDB tables match the expected schema definitions.

**Usage:**

```bash
# Validate all tables
python validate_schemas.py

# Validate specific table
python validate_schemas.py --table users

# Validate with custom prefix
python validate_schemas.py --prefix voice-for-bharat-prod
```

**Validation Checks:**
- Table existence
- Key schema (partition key, sort key)
- Global Secondary Indexes (name, keys, types)
- Attribute definitions and types
- TTL configuration
- Billing mode (On-Demand)
- Encryption settings
- Point-in-Time Recovery

**Example Output:**

```
Validating DynamoDB Schemas (Prefix: voice-for-bharat-dev)
================================================================================

Validating users... ✓ PASS

Validating schemes... ✓ PASS

Validating applications... ✓ PASS

Validating activity-log... ✓ PASS

Validating user-profile... ✓ PASS

Validating helplines... ✓ PASS

Validating guide-content... ✓ PASS

Validating suggested-queries... ✓ PASS

================================================================================
Summary: 8/8 tables passed validation

✓ All tables passed validation!
```

**Error Example:**

```
Validating users... ✗ FAIL
  - GSI phoneNumber-index: Missing sort key phoneNumber
  - Billing mode should be PAY_PER_REQUEST but is PROVISIONED
  - Point-in-Time Recovery should be enabled but is DISABLED
```

---

## Common Tasks

### Check if all tables are deployed

```bash
python manage_tables.py validate
```

This will show which tables exist and their configuration status.

### Verify table schemas match requirements

```bash
python validate_schemas.py
```

This performs comprehensive schema validation against expected definitions.

### Get detailed information about a table

```bash
python manage_tables.py describe users
```

### Check table status and item counts

```bash
python manage_tables.py status
```

### List all tables in an environment

```bash
# Development
python manage_tables.py list --prefix voice-for-bharat-dev

# Staging
python manage_tables.py list --prefix voice-for-bharat-staging

# Production
python manage_tables.py list --prefix voice-for-bharat-production
```

---

## Environment-Specific Usage

### Development

```bash
export TABLE_PREFIX=voice-for-bharat-dev
python manage_tables.py validate
python validate_schemas.py --prefix voice-for-bharat-dev
```

### Staging

```bash
export TABLE_PREFIX=voice-for-bharat-staging
python manage_tables.py validate
python validate_schemas.py --prefix voice-for-bharat-staging
```

### Production

```bash
export TABLE_PREFIX=voice-for-bharat-production
python manage_tables.py validate
python validate_schemas.py --prefix voice-for-bharat-production
```

---

## Troubleshooting

### "Table not found" error

Ensure:
1. AWS credentials are configured correctly
2. You have the correct AWS region set
3. The table prefix matches your environment
4. Tables have been deployed via SAM/CloudFormation

```bash
# Check AWS configuration
aws sts get-caller-identity
aws configure get region

# List all tables (no prefix filter)
aws dynamodb list-tables
```

### Permission errors

Ensure your IAM user/role has the following permissions:
- `dynamodb:DescribeTable`
- `dynamodb:ListTables`
- `dynamodb:DescribeTimeToLive`
- `dynamodb:DescribeContinuousBackups`
- `dynamodb:ListTagsOfResource`

### Schema validation failures

If validation fails:
1. Check the error messages for specific issues
2. Compare with the expected schema in `validate_schemas.py`
3. Review the SAM template (`backend/template.yaml`)
4. Redeploy the stack if necessary

```bash
# Redeploy SAM stack
cd backend
sam build
sam deploy --guided
```

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Validate DynamoDB Schemas
  run: |
    cd backend/scripts
    python validate_schemas.py --prefix voice-for-bharat-${{ env.ENVIRONMENT }}
```

### Pre-deployment Check

```bash
#!/bin/bash
# pre-deploy.sh

echo "Validating DynamoDB schemas before deployment..."
python backend/scripts/validate_schemas.py --prefix voice-for-bharat-dev

if [ $? -eq 0 ]; then
  echo "✓ Schema validation passed"
  exit 0
else
  echo "✗ Schema validation failed"
  exit 1
fi
```

---

## Additional Resources

- [DynamoDB Schema Documentation](../docs/DYNAMODB_SCHEMAS.md)
- [SAM Template](../template.yaml)
- [AWS DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)

---

## Support

For issues or questions:
1. Check the [DynamoDB Schema Documentation](../docs/DYNAMODB_SCHEMAS.md)
2. Review the SAM template for table definitions
3. Consult AWS DynamoDB documentation
4. Contact the development team


### 4. setup_s3_buckets.py

Set up and verify S3 bucket structure and policies.

**Usage:**
```bash
# Set up S3 buckets (verify + create folder structure)
python setup_s3_buckets.py --environment dev

# Verify only (no changes)
python setup_s3_buckets.py --environment dev --verify-only

# Use different region
python setup_s3_buckets.py --environment production --region us-east-1
```

**Options:**
- `--environment`: Environment (dev, staging, production) - **required**
- `--region`: AWS region (default: ap-south-1)
- `--verify-only`: Only verify configuration, do not create folder structure

**What it does:**
- Verifies S3 buckets exist
- Checks encryption configuration (SSE-S3)
- Verifies lifecycle policies
- Checks CORS configuration
- Verifies versioning (for documents and scheme-dumps buckets)
- Creates folder structure with placeholder files
- Tests presigned URL generation

**Example Output:**
```
================================================================================
S3 BUCKET VERIFICATION
================================================================================
Environment: dev
Region: ap-south-1
Account ID: 123456789012
================================================================================

📦 Checking DOCUMENTS bucket: voice-for-bharat-documents-dev-123456789012
--------------------------------------------------------------------------------
✓ Bucket exists: voice-for-bharat-documents-dev-123456789012
  ✓ Encryption enabled (SSE-S3)
  ✓ Lifecycle policies configured
    - TransitionToIA: Enabled
    - TransitionToGlacier: Enabled
    - DeleteAfter7Years: Enabled
  ✓ CORS configured
  ✓ Versioning enabled

✓ All checks passed for documents bucket

================================================================================
SUMMARY
================================================================================
✓ PASS: documents bucket
✓ PASS: audio bucket
✓ PASS: scheme-dumps bucket
================================================================================

✓ All buckets are properly configured!
```

## Updated Common Workflows

### Initial Setup

1. Deploy CloudFormation stack (creates all resources)
2. Verify infrastructure:
   ```bash
   python verify_infrastructure.py --environment dev
   ```
3. **Set up S3 buckets:**
   ```bash
   python setup_s3_buckets.py --environment dev
   ```
4. Validate schemas:
   ```bash
   python validate_schemas.py
   ```

### Daily Operations

- Check table status: `python manage_tables.py --action list --environment dev`
- **Verify S3 configuration:** `python setup_s3_buckets.py --environment dev --verify-only`
- Validate new models: `python validate_schemas.py --model NewModel`

### Troubleshooting

- Infrastructure issues: `python verify_infrastructure.py --environment dev --report`
- Table issues: `python manage_tables.py --action describe --environment dev --table users`
- **S3 issues:** `python setup_s3_buckets.py --environment dev --verify-only`
