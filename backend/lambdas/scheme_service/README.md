# Scheme Service Lambda

The Scheme Service manages government welfare scheme data, eligibility matching, and personalized recommendations for the Voice for Bharat platform.

## Features

- **Scheme Search**: Filter schemes by state, category, and active status
- **Multilingual Support**: Scheme content in 6 Indian languages (English, Hindi, Marathi, Kannada, Tamil, Telugu)
- **Eligibility Checking**: Calculate eligibility scores (0-100) based on user profile
- **Personalized Recommendations**: AI-powered scheme recommendations using user profile
- **Caching**: ElastiCache (Redis) integration for frequently accessed schemes
- **Government API Sync**: Sync scheme data from external government portals

## Architecture

```
┌─────────────────┐
│   API Gateway   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  Scheme Service │─────▶│  DynamoDB    │
│     Lambda      │      │   schemes    │
└────────┬────────┘      └──────────────┘
         │
         ├──────────────▶ ┌──────────────┐
         │                │ ElastiCache  │
         │                │   (Redis)    │
         │                └──────────────┘
         │
         └──────────────▶ ┌──────────────┐
                          │   Bedrock    │
                          │ (Embeddings) │
                          └──────────────┘
```

## API Endpoints

### GET /schemes

Search schemes with filters.

**Query Parameters:**
- `state` (optional): State code (e.g., "KA", "MH", "ALL_INDIA")
- `category` (optional): Scheme category (education, health, agriculture, etc.)
- `is_active` (optional): Filter for active schemes only (default: true)
- `user_id` (optional): User ID for eligibility scoring
- `language` (optional): Language code (default: "en")
- `limit` (optional): Maximum results (1-100, default: 50)

**Response:**
```json
{
  "success": true,
  "count": 10,
  "schemes": [
    {
      "scheme_id": "scheme-123",
      "name": "PM-KISAN Scheme",
      "description": "Direct income support to farmers",
      "state": "ALL_INDIA",
      "category": "agriculture",
      "benefits": "₹6,000 per year in three installments",
      "eligibility_score": 85,
      "match_reasons": ["Income below threshold", "Owns agricultural land"],
      "missing_info": []
    }
  ]
}
```

### GET /schemes/{scheme_id}

Get scheme details by ID.

**Path Parameters:**
- `scheme_id`: Unique scheme identifier

**Query Parameters:**
- `language` (optional): Language code (default: "en")
- `user_id` (optional): User ID for eligibility calculation

**Response:**
```json
{
  "success": true,
  "scheme": {
    "scheme_id": "scheme-123",
    "name": "PM-KISAN Scheme",
    "description": "Direct income support to farmers",
    "state": "ALL_INDIA",
    "category": "agriculture",
    "benefits": "₹6,000 per year in three installments",
    "application_process": [
      "Visit PM-KISAN portal",
      "Register with Aadhaar",
      "Submit land records",
      "Verify bank account"
    ],
    "required_documents": ["aadhaar", "land_records", "bank_passbook"],
    "portal_url": "https://pmkisan.gov.in",
    "portal_status": "ACTIVE",
    "eligibility_score": 85,
    "match_reasons": ["Income below threshold", "Owns agricultural land"],
    "missing_info": []
  }
}
```

### POST /schemes/{scheme_id}/check-eligibility

Check user eligibility for a scheme.

**Path Parameters:**
- `scheme_id`: Unique scheme identifier

**Request Body:**
```json
{
  "user_profile": {
    "date_of_birth": "1985-05-15",
    "gender": "MALE",
    "state": "KA",
    "income": 150000,
    "category": "GENERAL"
  }
}
```

**Response:**
```json
{
  "scheme_id": "scheme-123",
  "score": 85,
  "match_reasons": [
    "Age 38 is within eligible range (18-∞)",
    "Gender MALE is eligible",
    "Income ₹150,000 is below limit of ₹200,000",
    "Category GENERAL is eligible",
    "Scheme is available in KA"
  ],
  "missing_info": []
}
```

### POST /schemes/{scheme_id}/save

Save scheme to user's saved list.

**Path Parameters:**
- `scheme_id`: Unique scheme identifier

**Request Body:**
```json
{
  "user_id": "user-123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Scheme saved successfully",
  "scheme_id": "scheme-123",
  "saved_schemes_count": 5
}
```

### GET /schemes/recommendations

Get personalized scheme recommendations.

**Query Parameters:**
- `user_id` (required): User identifier
- `state` (optional): State code filter
- `language` (optional): Language code (default: "en")
- `limit` (optional): Maximum recommendations (1-50, default: 10)

**Response:**
```json
{
  "success": true,
  "count": 10,
  "recommendations": [
    {
      "scheme_id": "scheme-123",
      "name": "PM-KISAN Scheme",
      "eligibility_score": 95,
      "match_reasons": ["..."]
    }
  ]
}
```

### POST /schemes/sync

Sync scheme data from government APIs (admin only).

**Request Body:**
```json
{
  "source_url": "https://api.india.gov.in/schemes"
}
```

**Response:**
```json
{
  "success": true,
  "sync_result": {
    "status": "success",
    "schemes_added": 10,
    "schemes_updated": 25,
    "schemes_deactivated": 2,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## Eligibility Scoring Algorithm

The eligibility score is calculated based on multiple criteria:

1. **Age (20 points)**: User's age falls within scheme's age range
2. **Gender (15 points)**: User's gender matches eligible genders
3. **Income (25 points)**: User's income is below scheme's income limit
4. **Category (20 points)**: User's social category matches eligible categories
5. **State (20 points)**: Scheme is available in user's state
6. **Custom Rules (bonus)**: Additional criteria specific to the scheme

**Total: 100 points**

### Scoring Logic

- Each criterion is evaluated independently
- Missing user information results in 0 points for that criterion
- Custom rules can add bonus points beyond 100
- Final score is normalized to 0-100 range

### Match Reasons

The algorithm provides detailed reasons for eligibility:
- "Age 38 is within eligible range (18-60)"
- "Income ₹150,000 is below limit of ₹200,000"
- "Category SC is eligible"
- "Scheme is available in Karnataka"

### Missing Information

The algorithm identifies missing data needed for full eligibility:
- "Date of birth not provided"
- "Income information not provided"
- "Age 65 is outside eligible range (18-60)"

## Caching Strategy

The service uses ElastiCache (Redis) for caching:

- **Scheme List**: Cached by state, category, and language (1 hour TTL)
- **Scheme Details**: Cached by scheme_id and language (1 hour TTL)
- **Cache Keys**: `schemes:{state}:{category}:{is_active}:{language}`

### Cache Invalidation

Cache is automatically invalidated:
- After 1 hour (TTL expiration)
- When scheme data is synced from government APIs
- When scheme is updated manually

## DynamoDB Schema

### schemes Table

**Primary Key**: `scheme_id` (String)

**Global Secondary Indexes**:
- GSI1: `state` + `category` → For filtering schemes
- GSI2: `isActive` + `lastSyncedAt` → For sync operations
- GSI3: `category` + `viewCount` → For popular schemes

**Attributes**:
- `scheme_id`: Unique identifier
- `name`: Multilingual map (en, hi, mr, kn, ta, te)
- `description`: Multilingual map
- `state`: State code or "ALL_INDIA"
- `category`: Scheme category
- `eligibility_criteria`: Nested object with age, gender, income, category, states, custom_rules
- `benefits`: Multilingual map
- `application_process`: Multilingual map of step arrays
- `required_documents`: Array of document types
- `portal_url`: Government portal URL
- `portal_status`: ACTIVE, MAINTENANCE, or OFFLINE
- `is_active`: Boolean
- `last_synced_at`: ISO 8601 timestamp

## Lambda Configuration

- **Runtime**: Python 3.11
- **Architecture**: arm64 (Graviton2)
- **Memory**: 1GB
- **Timeout**: 60 seconds
- **Environment Variables**:
  - `AWS_REGION`: AWS region (default: ap-south-1)
  - `DYNAMODB_TABLE_PREFIX`: Table name prefix (default: voice-for-bharat)
  - `REDIS_HOST`: ElastiCache Redis endpoint
  - `REDIS_PORT`: Redis port (default: 6379)

## Dependencies

- `fastapi==0.104.1`: Web framework
- `pydantic==2.5.0`: Data validation
- `boto3==1.34.0`: AWS SDK
- `mangum==0.17.0`: ASGI adapter for Lambda
- `redis==5.0.1`: Redis client for caching

## Development

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AWS_REGION=ap-south-1
export DYNAMODB_TABLE_PREFIX=voice-for-bharat-dev
export REDIS_HOST=localhost

# Run FastAPI locally
uvicorn handler:app --reload --port 8002
```

### Testing Endpoints

```bash
# Search schemes
curl "http://localhost:8002/schemes?state=KA&category=agriculture&language=en"

# Get scheme details
curl "http://localhost:8002/schemes/scheme-123?language=hi&user_id=user-456"

# Check eligibility
curl -X POST "http://localhost:8002/schemes/scheme-123/check-eligibility" \
  -H "Content-Type: application/json" \
  -d '{"user_profile": {"date_of_birth": "1985-05-15", "gender": "MALE", "state": "KA", "income": 150000, "category": "GENERAL"}}'

# Save scheme
curl -X POST "http://localhost:8002/schemes/scheme-123/save" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user-456"}'

# Get recommendations
curl "http://localhost:8002/schemes/recommendations?user_id=user-456&limit=10"
```

## Deployment

```bash
# Build and deploy with SAM
cd backend
sam build
sam deploy --guided

# Or use AWS CLI
aws lambda update-function-code \
  --function-name voice-for-bharat-scheme-service \
  --zip-file fileb://scheme_service.zip
```

## Monitoring

- **CloudWatch Logs**: `/aws/lambda/voice-for-bharat-scheme-service`
- **CloudWatch Metrics**: 
  - Invocations
  - Duration
  - Errors
  - Throttles
- **Custom Metrics**:
  - Scheme searches per minute
  - Eligibility checks per minute
  - Cache hit rate
  - Average eligibility score

## Error Handling

The service returns standard HTTP error codes:

- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Scheme not found
- `500 Internal Server Error`: Server-side error

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Security

- **IAM Roles**: Lambda execution role with minimal permissions
- **DynamoDB**: Read-only access to schemes table, read-write to user_profile
- **S3**: No direct S3 access required
- **Bedrock**: Access to embeddings model for recommendations
- **ElastiCache**: VPC-based access to Redis cluster

## Future Enhancements

1. **Vector Search**: Implement OpenSearch Serverless for semantic scheme search
2. **ML Recommendations**: Use Bedrock Agents for intelligent recommendations
3. **Real-time Sync**: WebSocket-based real-time scheme updates
4. **Analytics**: Track popular schemes and user preferences
5. **A/B Testing**: Test different eligibility scoring algorithms
