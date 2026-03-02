# User Service Lambda

User Service handles user registration, authentication via phone number OTP, and profile management for Voice for Bharat.

## Features

- User registration with phone number
- OTP-based authentication via AWS Cognito
- User profile management (CRUD operations)
- Profile strength calculation
- Integration with DynamoDB for user data storage

## API Endpoints

### POST /register
Register a new user or initiate OTP for existing user.

**Request:**
```json
{
  "phone_number": "9876543210",
  "language": "en"
}
```

**Response:**
```json
{
  "user_id": "uuid",
  "phone_number": "9876543210",
  "message": "OTP sent to your phone number"
}
```

### POST /verify-otp
Verify OTP and authenticate user.

**Request:**
```json
{
  "phone_number": "9876543210",
  "otp": "123456"
}
```

**Response:**
```json
{
  "user_id": "uuid",
  "access_token": "jwt_token",
  "refresh_token": "jwt_token",
  "id_token": "jwt_token",
  "message": "Authentication successful"
}
```

### GET /profile/{user_id}
Get user profile by user ID.

**Response:**
```json
{
  "user_id": "uuid",
  "phone_number": "9876543210",
  "language": "en",
  "profile": {
    "name": "John Doe",
    "date_of_birth": "1990-01-01T00:00:00",
    "gender": "MALE",
    "state": "MH",
    "district": "Mumbai",
    "income": 50000,
    "category": "GENERAL"
  },
  "preferences": {
    "notification_channels": ["sms"],
    "preferred_language": "en",
    "voice_speed": 1.0,
    "auto_play_audio": true
  },
  "profile_strength": 70,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login_at": "2024-01-01T00:00:00"
}
```

### PUT /profile/{user_id}
Update user profile.

**Request:**
```json
{
  "profile": {
    "name": "John Doe",
    "date_of_birth": "1990-01-01T00:00:00",
    "gender": "MALE",
    "state": "MH",
    "district": "Mumbai",
    "income": 50000,
    "category": "GENERAL",
    "aadhaar_number": "123456789012",
    "pan_number": "ABCDE1234F"
  }
}
```

**Response:** Same as GET /profile/{user_id}

## Environment Variables

- `COGNITO_USER_POOL_ID`: AWS Cognito User Pool ID
- `COGNITO_CLIENT_ID`: AWS Cognito App Client ID
- `AWS_REGION`: AWS region (default: ap-south-1)
- `DYNAMODB_TABLE_PREFIX`: DynamoDB table name prefix (default: voice-for-bharat)

## Lambda Configuration

- **Memory**: 512MB
- **Timeout**: 30 seconds
- **Runtime**: Python 3.11
- **Architecture**: arm64 (Graviton2)

## Dependencies

See `requirements.txt` for Python dependencies.

## Profile Strength Calculation

Profile strength is calculated as a percentage (0-100) based on:

- **Required fields (70% weight)**: name, date_of_birth, gender, state, district, income, category
- **Document fields (30% weight)**: aadhaar_number, pan_number, bank_account

Formula:
```
profile_strength = (filled_required / total_required) * 70 + (filled_documents / total_documents) * 30
```

## Phone Number Validation

Phone numbers must:
- Be 10 digits long
- Start with 6, 7, 8, or 9
- Be valid Indian mobile numbers

The service automatically adds +91 prefix for Cognito operations.

## Error Handling

The service returns appropriate HTTP status codes:
- `200 OK`: Successful operation
- `201 Created`: User registered successfully
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid OTP or authentication failed
- `404 Not Found`: User not found
- `409 Conflict`: User already exists
- `500 Internal Server Error`: Server-side error

## Testing

To test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run with uvicorn
uvicorn handler:app --reload --port 8000

# Test endpoints
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "9876543210", "language": "en"}'
```

## Deployment

Deploy using AWS SAM:

```bash
sam build
sam deploy --guided
```

Or use the deployment script:

```bash
cd backend
./deploy.sh user_service
```
