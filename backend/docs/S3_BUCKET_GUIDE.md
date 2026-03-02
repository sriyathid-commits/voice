# S3 Bucket Structure and Usage Guide

## Overview

Voice for Bharat uses three S3 buckets for storing different types of data:
1. **Documents Bucket** - User-uploaded documents (Aadhaar, PAN, certificates)
2. **Audio Bucket** - Voice recordings and TTS audio files
3. **Scheme Dumps Bucket** - Scheme data backups and dumps

All buckets use SSE-S3 encryption, block public access, and have configured lifecycle policies for cost optimization.

## Bucket Naming Convention

Buckets follow the naming pattern: `voice-for-bharat-{type}-{environment}-{account-id}`

Examples:
- `voice-for-bharat-documents-dev-123456789012`
- `voice-for-bharat-audio-production-123456789012`
- `voice-for-bharat-scheme-dumps-staging-123456789012`

## 1. Documents Bucket

### Purpose
Store user-uploaded documents required for scheme applications and profile verification.

### Bucket Name
`voice-for-bharat-documents-{environment}-{account-id}`

### Folder Structure

```
voice-for-bharat-documents-{env}-{account-id}/
├── users/
│   └── {userId}/
│       ├── aadhaar/
│       │   └── {documentId}.pdf
│       ├── pan/
│       │   └── {documentId}.pdf
│       ├── income-certificate/
│       │   └── {documentId}.pdf
│       ├── caste-certificate/
│       │   └── {documentId}.pdf
│       ├── bank-passbook/
│       │   └── {documentId}.pdf
│       ├── photos/
│       │   └── {documentId}.jpg
│       ├── domicile-certificate/
│       │   └── {documentId}.pdf
│       ├── age-proof/
│       │   └── {documentId}.pdf
│       ├── land-records/
│       │   └── {documentId}.pdf
│       └── disability-certificate/
│           └── {documentId}.pdf
└── applications/
    └── {applicationId}/
        └── {documentType}/
            └── {documentId}.pdf
```

### Security Configuration

- **Encryption**: SSE-S3 (AES-256)
- **Versioning**: Enabled
- **Public Access**: Blocked
- **Access Method**: Presigned URLs (15-minute expiration)

### Lifecycle Policies

| Rule ID | Action | Timeline |
|---------|--------|----------|
| TransitionToIA | Move to S3 Infrequent Access | After 90 days |
| TransitionToGlacier | Move to Glacier | After 365 days |
| DeleteAfter7Years | Permanent deletion | After 2555 days (7 years) |

### CORS Configuration

```json
{
  "AllowedOrigins": ["*"],
  "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
  "AllowedHeaders": ["*"],
  "MaxAge": 3000
}
```

### Usage Examples

#### Upload Document

```python
from backend.shared.utils import get_document_s3_key, upload_to_s3
import os

# Generate S3 key
s3_key = get_document_s3_key(
    user_id="user-123",
    document_type="aadhaar",
    document_id="doc-456",
    extension="pdf"
)
# Result: "users/user-123/aadhaar/doc-456.pdf"

# Upload document
bucket = os.getenv("S3_DOCUMENTS_BUCKET")
success = upload_to_s3(
    bucket=bucket,
    key=s3_key,
    data=document_bytes,
    content_type="application/pdf",
    metadata={
        "user_id": "user-123",
        "document_type": "aadhaar",
        "uploaded_at": "2024-01-15T10:30:00Z"
    }
)
```

#### Generate Presigned URL for Download

```python
from backend.shared.utils import generate_presigned_url
import os

bucket = os.getenv("S3_DOCUMENTS_BUCKET")
s3_key = "users/user-123/aadhaar/doc-456.pdf"

# Generate URL valid for 15 minutes
url = generate_presigned_url(
    bucket=bucket,
    key=s3_key,
    expiration=900
)
```

#### Generate Presigned POST for Direct Upload

```python
from backend.shared.utils import generate_presigned_post
import os

bucket = os.getenv("S3_DOCUMENTS_BUCKET")
s3_key = "users/user-123/pan/doc-789.pdf"

# Generate presigned POST for browser upload
post_data = generate_presigned_post(
    bucket=bucket,
    key=s3_key,
    expiration=900,
    max_size=5242880  # 5MB
)

# Returns: {"url": "https://...", "fields": {...}}
```

## 2. Audio Bucket

### Purpose
Store voice recordings, TTS audio responses, and STT recordings for voice assistant functionality.

### Bucket Name
`voice-for-bharat-audio-{environment}-{account-id}`

### Folder Structure

```
voice-for-bharat-audio-{env}-{account-id}/
├── conversations/
│   └── {sessionId}/
│       ├── user/
│       │   └── {messageId}.wav
│       └── assistant/
│           └── {messageId}.mp3
├── tts-cache/
│   └── {language}/
│       └── {textHash}.mp3
└── stt-recordings/
    └── {userId}/
        └── {timestamp}.wav
```

### Security Configuration

- **Encryption**: SSE-S3 (AES-256)
- **Versioning**: Disabled (not needed for temporary audio)
- **Public Access**: Blocked
- **Access Method**: CloudFront CDN with presigned URLs

### Lifecycle Policies

| Rule ID | Prefix | Action | Timeline |
|---------|--------|--------|----------|
| DeleteConversationsAfter30Days | conversations/ | Delete | After 30 days |
| DeleteTTSCacheAfter90Days | tts-cache/ | Delete | After 90 days |
| DeleteSTTRecordingsAfter7Days | stt-recordings/ | Delete | After 7 days |

### CORS Configuration

```json
{
  "AllowedOrigins": ["*"],
  "AllowedMethods": ["GET", "PUT", "POST"],
  "AllowedHeaders": ["*"],
  "MaxAge": 3000
}
```

### Usage Examples

#### Store Conversation Audio

```python
from backend.shared.utils import get_audio_s3_key, upload_to_s3
import os

# User audio (WAV format)
user_key = get_audio_s3_key(
    session_id="session-123",
    role="user",
    message_id="msg-456",
    extension="wav"
)
# Result: "conversations/session-123/user/msg-456.wav"

bucket = os.getenv("S3_AUDIO_BUCKET")
upload_to_s3(bucket, user_key, audio_bytes, "audio/wav")

# Assistant audio (MP3 format)
assistant_key = get_audio_s3_key(
    session_id="session-123",
    role="assistant",
    message_id="msg-457",
    extension="mp3"
)
# Result: "conversations/session-123/assistant/msg-457.mp3"

upload_to_s3(bucket, assistant_key, audio_bytes, "audio/mpeg")
```

#### Cache TTS Audio

```python
from backend.shared.utils import get_tts_cache_s3_key, hash_text, upload_to_s3
import os

text = "नमस्ते, आपकी कैसे मदद कर सकता हूं?"
text_hash = hash_text(text)

cache_key = get_tts_cache_s3_key(
    language="hi",
    text_hash=text_hash
)
# Result: "tts-cache/hi/{hash}.mp3"

bucket = os.getenv("S3_AUDIO_BUCKET")
upload_to_s3(bucket, cache_key, tts_audio_bytes, "audio/mpeg")
```

#### Get Audio via CloudFront

```python
from backend.shared.utils import generate_presigned_url
import os

# Audio is served via CloudFront for better performance
cloudfront_url = os.getenv("CLOUDFRONT_URL")
s3_key = "conversations/session-123/assistant/msg-457.mp3"

# For CloudFront, use the bucket as origin
bucket = os.getenv("S3_AUDIO_BUCKET")
presigned_url = generate_presigned_url(bucket, s3_key, expiration=3600)
```

## 3. Scheme Dumps Bucket

### Purpose
Store backups of scheme data synced from government APIs and external sources.

### Bucket Name
`voice-for-bharat-scheme-dumps-{environment}-{account-id}`

### Folder Structure

```
voice-for-bharat-scheme-dumps-{env}-{account-id}/
├── daily/
│   └── {YYYY-MM-DD}/
│       └── schemes.json
├── weekly/
│   └── {YYYY-WW}/
│       └── schemes-full.json
└── sources/
    └── {source-name}/
        └── {timestamp}.json
```

### Security Configuration

- **Encryption**: SSE-S3 (AES-256)
- **Versioning**: Enabled
- **Public Access**: Blocked
- **Access Method**: Direct S3 access (internal only)

### Lifecycle Policies

| Rule ID | Prefix | Action | Timeline |
|---------|--------|--------|----------|
| DeleteDailyDumpsAfter30Days | daily/ | Delete | After 30 days |
| DeleteWeeklyDumpsAfter1Year | weekly/ | Delete | After 365 days |
| ArchiveSourceDataToGlacier | sources/ | Move to Glacier | After 90 days |

### Usage Examples

#### Store Daily Scheme Dump

```python
from backend.shared.utils import upload_to_s3
from datetime import datetime
import json
import os

# Generate daily dump key
date_str = datetime.now().strftime("%Y-%m-%d")
s3_key = f"daily/{date_str}/schemes.json"

# Prepare scheme data
schemes_data = {
    "sync_timestamp": datetime.now().isoformat(),
    "total_schemes": 1234,
    "schemes": [...]
}

bucket = os.getenv("S3_SCHEME_DUMPS_BUCKET")
upload_to_s3(
    bucket=bucket,
    key=s3_key,
    data=json.dumps(schemes_data).encode('utf-8'),
    content_type="application/json",
    metadata={
        "sync_date": date_str,
        "scheme_count": str(len(schemes_data["schemes"]))
    }
)
```

#### Store Source Data

```python
from backend.shared.utils import upload_to_s3
from datetime import datetime
import json
import os

# Store raw data from government API
source_name = "national-portal"
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
s3_key = f"sources/{source_name}/{timestamp}.json"

bucket = os.getenv("S3_SCHEME_DUMPS_BUCKET")
upload_to_s3(
    bucket=bucket,
    key=s3_key,
    data=json.dumps(raw_api_data).encode('utf-8'),
    content_type="application/json",
    metadata={
        "source": source_name,
        "sync_timestamp": timestamp
    }
)
```

## IAM Permissions

### Lambda Execution Role Permissions

The Lambda execution role has the following S3 permissions:

```yaml
- Effect: Allow
  Action:
    - s3:GetObject
    - s3:PutObject
    - s3:DeleteObject
  Resource:
    - arn:aws:s3:::voice-for-bharat-documents-*/*
    - arn:aws:s3:::voice-for-bharat-audio-*/*
    - arn:aws:s3:::voice-for-bharat-scheme-dumps-*/*

- Effect: Allow
  Action:
    - s3:ListBucket
  Resource:
    - arn:aws:s3:::voice-for-bharat-documents-*
    - arn:aws:s3:::voice-for-bharat-audio-*
    - arn:aws:s3:::voice-for-bharat-scheme-dumps-*
```

## CloudFront Integration

The Audio Bucket is integrated with CloudFront for optimized content delivery:

- **Origin**: S3 Audio Bucket
- **Origin Access Identity**: Configured for secure access
- **Viewer Protocol**: HTTPS redirect
- **Caching**: Default TTL 24 hours, Max TTL 1 year
- **Compression**: Enabled
- **Price Class**: All edge locations

### CloudFront URL Format

```
https://{distribution-id}.cloudfront.net/conversations/{sessionId}/assistant/{messageId}.mp3
```

## Best Practices

### 1. Document Storage

- Always use presigned URLs for document access
- Set appropriate expiration times (15 minutes for downloads)
- Include metadata for tracking and auditing
- Validate file types and sizes before upload
- Use consistent naming conventions

### 2. Audio Storage

- Cache TTS responses to reduce Bedrock costs
- Use CloudFront for audio delivery
- Clean up temporary recordings after processing
- Use appropriate audio formats (WAV for input, MP3 for output)

### 3. Scheme Dumps

- Perform daily incremental backups
- Perform weekly full backups
- Store raw source data for audit trail
- Use versioning for critical data
- Archive old data to Glacier

### 4. Security

- Never make buckets public
- Always use presigned URLs for client access
- Rotate presigned URLs frequently
- Encrypt sensitive documents at application level
- Monitor S3 access logs

### 5. Cost Optimization

- Use lifecycle policies to transition old data
- Delete temporary files promptly
- Use S3 Intelligent-Tiering for unpredictable access patterns
- Monitor storage metrics and adjust policies

## Monitoring and Alerts

### CloudWatch Metrics to Monitor

- **BucketSizeBytes** - Track storage growth
- **NumberOfObjects** - Track object count
- **AllRequests** - Monitor request volume
- **4xxErrors** - Track client errors
- **5xxErrors** - Track server errors

### Recommended Alarms

1. **High Error Rate**: Alert if 4xx/5xx errors exceed threshold
2. **Storage Growth**: Alert if bucket size grows unexpectedly
3. **Request Spike**: Alert if request rate exceeds normal patterns
4. **Lifecycle Failures**: Alert if lifecycle policies fail

## Troubleshooting

### Common Issues

#### 1. Access Denied Errors

**Symptom**: 403 Forbidden when accessing objects

**Solutions**:
- Verify IAM role has correct permissions
- Check bucket policy doesn't block access
- Ensure presigned URL hasn't expired
- Verify object exists in bucket

#### 2. CORS Errors

**Symptom**: Browser blocks S3 requests

**Solutions**:
- Verify CORS configuration is correct
- Check AllowedOrigins includes your domain
- Ensure AllowedMethods includes required methods
- Clear browser cache

#### 3. Lifecycle Policy Not Working

**Symptom**: Objects not transitioning or deleting

**Solutions**:
- Verify lifecycle rules are enabled
- Check rule filters match object keys
- Wait for daily lifecycle evaluation
- Check CloudWatch logs for errors

#### 4. Presigned URL Fails

**Symptom**: Presigned URL returns error

**Solutions**:
- Check URL hasn't expired
- Verify object exists at specified key
- Ensure IAM role has GetObject permission
- Check for special characters in key

## Setup and Verification

### Initial Setup

1. Deploy CloudFormation stack (creates buckets)
2. Run setup script to create folder structure:
   ```bash
   python backend/scripts/setup_s3_buckets.py --environment dev
   ```
3. Verify configuration:
   ```bash
   python backend/scripts/setup_s3_buckets.py --environment dev --verify-only
   ```

### Verification Checklist

- [ ] All three buckets exist
- [ ] SSE-S3 encryption enabled
- [ ] Lifecycle policies configured
- [ ] CORS policies configured
- [ ] Versioning enabled (documents and scheme-dumps)
- [ ] Public access blocked
- [ ] CloudFront distribution configured
- [ ] Presigned URL generation works
- [ ] Folder structure created

## References

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [S3 Lifecycle Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [S3 Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html)
- [CloudFront with S3](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
