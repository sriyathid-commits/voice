# S3 Quick Reference Guide

Quick reference for common S3 operations in Voice for Bharat.

## Import Utilities

```python
from backend.shared import (
    # S3 key generators
    get_document_s3_key,
    get_application_document_s3_key,
    get_audio_s3_key,
    get_tts_cache_s3_key,
    get_stt_recording_s3_key,
    # S3 operations
    upload_to_s3,
    download_from_s3,
    delete_from_s3,
    check_s3_object_exists,
    # Presigned URLs
    generate_presigned_url,
    generate_presigned_post,
    # Other utilities
    hash_text
)
import os
```

## Common Operations

### 1. Upload User Document

```python
# Generate S3 key
s3_key = get_document_s3_key(
    user_id="user-123",
    document_type="aadhaar",
    document_id="doc-456",
    extension="pdf"
)

# Upload to S3
bucket = os.getenv("S3_DOCUMENTS_BUCKET")
success = upload_to_s3(
    bucket=bucket,
    key=s3_key,
    data=pdf_bytes,
    content_type="application/pdf",
    metadata={
        "user_id": "user-123",
        "document_type": "aadhaar"
    }
)
```

### 2. Generate Download URL

```python
# For documents
bucket = os.getenv("S3_DOCUMENTS_BUCKET")
s3_key = "users/user-123/aadhaar/doc-456.pdf"

url = generate_presigned_url(
    bucket=bucket,
    key=s3_key,
    expiration=900  # 15 minutes
)
```

### 3. Direct Browser Upload

```python
# Generate presigned POST
bucket = os.getenv("S3_DOCUMENTS_BUCKET")
s3_key = get_document_s3_key("user-123", "pan", "doc-789", "pdf")

post_data = generate_presigned_post(
    bucket=bucket,
    key=s3_key,
    expiration=900,
    max_size=5242880  # 5MB
)

# Return to frontend
return {
    "upload_url": post_data["url"],
    "upload_fields": post_data["fields"],
    "s3_key": s3_key
}
```

### 4. Store Conversation Audio

```python
# User audio (WAV)
user_key = get_audio_s3_key(
    session_id="session-123",
    role="user",
    message_id="msg-456",
    extension="wav"
)

bucket = os.getenv("S3_AUDIO_BUCKET")
upload_to_s3(bucket, user_key, wav_bytes, "audio/wav")

# Assistant audio (MP3)
assistant_key = get_audio_s3_key(
    session_id="session-123",
    role="assistant",
    message_id="msg-457",
    extension="mp3"
)

upload_to_s3(bucket, assistant_key, mp3_bytes, "audio/mpeg")
```

### 5. Cache TTS Audio

```python
# Generate cache key
text = "नमस्ते, आपकी कैसे मदद कर सकता हूं?"
text_hash = hash_text(text)

cache_key = get_tts_cache_s3_key(
    language="hi",
    text_hash=text_hash
)

# Check if cached
bucket = os.getenv("S3_AUDIO_BUCKET")
if check_s3_object_exists(bucket, cache_key):
    # Use cached audio
    audio_bytes = download_from_s3(bucket, cache_key)
else:
    # Generate new TTS and cache
    audio_bytes = generate_tts(text, "hi")
    upload_to_s3(bucket, cache_key, audio_bytes, "audio/mpeg")
```

### 6. Store Scheme Dump

```python
from datetime import datetime
import json

# Daily dump
date_str = datetime.now().strftime("%Y-%m-%d")
s3_key = f"daily/{date_str}/schemes.json"

schemes_data = {
    "sync_timestamp": datetime.now().isoformat(),
    "total_schemes": len(schemes),
    "schemes": schemes
}

bucket = os.getenv("S3_SCHEME_DUMPS_BUCKET")
upload_to_s3(
    bucket=bucket,
    key=s3_key,
    data=json.dumps(schemes_data).encode('utf-8'),
    content_type="application/json"
)
```

### 7. Delete Document

```python
bucket = os.getenv("S3_DOCUMENTS_BUCKET")
s3_key = "users/user-123/aadhaar/doc-456.pdf"

success = delete_from_s3(bucket, s3_key)
```

### 8. Check if Document Exists

```python
bucket = os.getenv("S3_DOCUMENTS_BUCKET")
s3_key = "users/user-123/aadhaar/doc-456.pdf"

exists = check_s3_object_exists(bucket, s3_key)
```

## Document Types

Valid document types for `get_document_s3_key()`:

- `aadhaar` - Aadhaar card
- `pan` - PAN card
- `income-certificate` - Income certificate
- `caste-certificate` - Caste certificate
- `bank-passbook` - Bank passbook
- `photo` - Passport photo
- `domicile-certificate` - Domicile certificate
- `age-proof` - Age proof document
- `land-records` - Land ownership records
- `disability-certificate` - Disability certificate

## File Extensions

Common file extensions:

- Documents: `pdf`, `jpg`, `jpeg`, `png`
- User audio: `wav`
- Assistant audio: `mp3`
- TTS cache: `mp3`

## Bucket Environment Variables

```python
# Documents bucket
S3_DOCUMENTS_BUCKET = os.getenv("S3_DOCUMENTS_BUCKET")

# Audio bucket
S3_AUDIO_BUCKET = os.getenv("S3_AUDIO_BUCKET")

# Scheme dumps bucket
S3_SCHEME_DUMPS_BUCKET = os.getenv("S3_SCHEME_DUMPS_BUCKET")

# CloudFront URL for audio delivery
CLOUDFRONT_URL = os.getenv("CLOUDFRONT_URL")
```

## Error Handling

```python
try:
    success = upload_to_s3(bucket, key, data, content_type)
    if not success:
        # Handle upload failure
        logger.error(f"Failed to upload to S3: {key}")
        return {"error": "Upload failed"}
except Exception as e:
    logger.error(f"S3 error: {e}")
    return {"error": str(e)}
```

## Best Practices

1. **Always use presigned URLs** for client access
2. **Set appropriate expiration times** (15 minutes for downloads)
3. **Include metadata** for tracking and auditing
4. **Validate file types and sizes** before upload
5. **Use consistent naming conventions** via utility functions
6. **Cache TTS responses** to reduce costs
7. **Clean up temporary files** after processing
8. **Check existence** before attempting operations
9. **Handle errors gracefully** with proper logging
10. **Use CloudFront** for audio delivery

## Security Notes

- Never make buckets public
- Always use presigned URLs for client access
- Rotate presigned URLs frequently (15-minute expiration)
- Encrypt sensitive documents at application level
- Monitor S3 access logs
- Validate file types before upload
- Limit file sizes (5MB for documents)

## Performance Tips

- Use CloudFront for frequently accessed audio
- Cache TTS responses by text hash
- Use multipart upload for large files (>5MB)
- Implement retry logic for failed uploads
- Use batch operations when possible
- Monitor S3 request metrics

## Troubleshooting

### Access Denied (403)
- Check IAM role permissions
- Verify presigned URL hasn't expired
- Ensure object exists in bucket

### CORS Errors
- Verify CORS configuration
- Check AllowedOrigins includes your domain
- Ensure AllowedMethods includes required methods

### Upload Fails
- Check file size limits
- Verify content type is correct
- Ensure bucket has space
- Check network connectivity

### Presigned URL Fails
- Verify URL hasn't expired (15 minutes)
- Check object exists at specified key
- Ensure IAM role has GetObject permission
