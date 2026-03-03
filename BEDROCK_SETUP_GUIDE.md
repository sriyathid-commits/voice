# Amazon Bedrock Setup Guide

## 🚀 Step 1: Request Model Access

### Go to Bedrock Console
**URL**: https://ap-south-1.console.aws.amazon.com/bedrock/home?region=ap-south-1#/modelaccess

### Request Access for These Models:

#### 1. **Anthropic Claude 3 Sonnet** (Required)
- Model ID: `anthropic.claude-3-sonnet-20240229-v1:0`
- Purpose: Natural language understanding, conversation
- Use case: Process user queries, extract intent
- **Click "Request model access"**

#### 2. **Amazon Titan Text G1 - Express** (Optional but recommended)
- Model ID: `amazon.titan-text-express-v1`
- Purpose: Text generation, embeddings
- Use case: Scheme search, semantic matching
- **Click "Request model access"**

#### 3. **Amazon Titan Multimodal Embeddings** (Optional)
- Model ID: `amazon.titan-embed-text-v1`
- Purpose: Vector embeddings for search
- Use case: Semantic scheme matching
- **Click "Request model access"**

---

## ⏱️ Access Approval Time

- **Instant**: Some models (Titan) are approved immediately
- **24-48 hours**: Claude models may require manual approval
- **Check status**: Refresh the model access page

---

## 🔍 Step 2: Verify Access

### Check Model Access Status
```bash
# List available models
python -m awscli bedrock list-foundation-models --region ap-south-1

# Check if Claude is accessible
python -m awscli bedrock list-foundation-models --region ap-south-1 --query "modelSummaries[?contains(modelId, 'claude')]"
```

### Test Bedrock Access
```bash
# Test invoke (after access granted)
python -m awscli bedrock-runtime invoke-model ^
  --model-id anthropic.claude-3-sonnet-20240229-v1:0 ^
  --body "{\"prompt\":\"Hello\",\"max_tokens\":100}" ^
  --region ap-south-1 ^
  output.json
```

---

## 📝 Step 3: Update IAM Permissions

### Add Bedrock Permissions to Lambda Roles

Go to IAM Console:
**URL**: https://console.aws.amazon.com/iam/home?region=ap-south-1#/roles

### Find Your Lambda Roles:
- `voicebharatai-UserServiceRole-xxxxx`
- `voicebharatai-VoiceServiceRole-xxxxx`
- `voicebharatai-SchemeServiceRole-xxxxx`

### Add This Policy to Each Role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:ap-south-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
        "arn:aws:bedrock:ap-south-1::foundation-model/amazon.titan-text-express-v1",
        "arn:aws:bedrock:ap-south-1::foundation-model/amazon.titan-embed-text-v1"
      ]
    }
  ]
}
```

### How to Add:
1. Click on role
2. Click "Add permissions" → "Create inline policy"
3. Click "JSON" tab
4. Paste the policy above
5. Name it: `BedrockAccessPolicy`
6. Click "Create policy"

---

## 🎯 Step 4: Update Lambda Environment Variables

### Add Bedrock Configuration

For each Lambda function, add these environment variables:

```
BEDROCK_REGION=ap-south-1
BEDROCK_CLAUDE_MODEL=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_TITAN_TEXT_MODEL=amazon.titan-text-express-v1
BEDROCK_TITAN_EMBED_MODEL=amazon.titan-embed-text-v1
```

### How to Add:
1. Go to Lambda console
2. Click on function (e.g., VoiceService)
3. Configuration → Environment variables
4. Click "Edit"
5. Add the variables above
6. Click "Save"

---

## 💻 Step 5: Update Voice Service Code

I'll update the code to use real Bedrock calls instead of mocks.

### Files to Update:
1. `backend/lambdas/voice_service/service.py` - Add real Bedrock calls
2. `backend/lambdas/voice_service/requirements.txt` - Add boto3 bedrock
3. `backend/shared/utils.py` - Add Bedrock helper functions

---

## 🧪 Step 6: Test Bedrock Integration

### Test Claude API
```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='ap-south-1')

# Test Claude
response = bedrock.invoke_model(
    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": "Hello, how are you?"
            }
        ]
    })
)

result = json.loads(response['body'].read())
print(result['content'][0]['text'])
```

---

## 💰 Bedrock Pricing (Important!)

### Claude 3 Sonnet Pricing:
- **Input**: $3 per 1M tokens (~750K words)
- **Output**: $15 per 1M tokens (~750K words)

### Example Costs:
- 100 conversations/day = ~$0.50-2/day
- 1000 conversations/day = ~$5-20/day
- 10,000 conversations/day = ~$50-200/day

### Cost Control:
1. Set up billing alerts
2. Use caching (Redis) to reduce API calls
3. Limit max_tokens in requests
4. Monitor usage in CloudWatch

---

## 🔐 Security Best Practices

### 1. Use IAM Roles (Not Access Keys)
- Lambda uses execution role
- No hardcoded credentials

### 2. Enable CloudWatch Logging
- Monitor all Bedrock API calls
- Track token usage
- Alert on errors

### 3. Implement Rate Limiting
- Prevent abuse
- Control costs
- Use API Gateway throttling

---

## 📊 Monitor Bedrock Usage

### CloudWatch Metrics
**URL**: https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#metricsV2:

**Metrics to watch:**
- `Bedrock/InvocationCount` - Number of API calls
- `Bedrock/InvocationLatency` - Response time
- `Bedrock/InvocationErrors` - Failed requests
- `Bedrock/TokensUsed` - Token consumption

### Set Up Alarms:
1. High token usage (cost control)
2. High error rate (quality monitoring)
3. High latency (performance)

---

## ⚠️ Important Notes

### 1. Model Availability
- Not all models available in all regions
- ap-south-1 (Mumbai) supports Claude 3 Sonnet ✅
- Check: https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html

### 2. Request Limits
- Claude 3 Sonnet: 200 requests/minute
- Titan models: 400 requests/minute
- Can request increase if needed

### 3. Token Limits
- Claude 3 Sonnet: 200K tokens context window
- Max output: 4096 tokens per request

---

## 🚀 Quick Start Commands

### 1. Request Model Access
```bash
# Open Bedrock console
start https://ap-south-1.console.aws.amazon.com/bedrock/home?region=ap-south-1#/modelaccess
```

### 2. Check Access Status
```bash
python -m awscli bedrock list-foundation-models --region ap-south-1 --query "modelSummaries[?contains(modelId, 'claude')].{ModelId:modelId,Status:modelLifecycle.status}"
```

### 3. Test Access
```bash
# Create test file
echo {"anthropic_version":"bedrock-2023-05-31","max_tokens":100,"messages":[{"role":"user","content":"Hello"}]} > test-input.json

# Invoke model
python -m awscli bedrock-runtime invoke-model --model-id anthropic.claude-3-sonnet-20240229-v1:0 --body file://test-input.json --region ap-south-1 output.json

# View response
type output.json
```

---

## 📞 Need Help?

### AWS Support
- **Free tier**: Community forums
- **Developer**: $29/month - Technical support
- **Business**: $100/month - 24/7 support

### Documentation
- Bedrock User Guide: https://docs.aws.amazon.com/bedrock/
- Claude API Reference: https://docs.anthropic.com/claude/reference/
- Boto3 Bedrock: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html

---

## ✅ Checklist

- [ ] Request Claude 3 Sonnet access
- [ ] Request Titan model access (optional)
- [ ] Wait for approval (check email)
- [ ] Verify access in console
- [ ] Add IAM permissions to Lambda roles
- [ ] Update Lambda environment variables
- [ ] Update code with real Bedrock calls
- [ ] Test with sample requests
- [ ] Set up billing alerts
- [ ] Monitor CloudWatch metrics

---

## 🎯 Next Steps

Once Bedrock access is approved:
1. I'll update the voice service code with real API calls
2. We'll test the integration
3. Deploy updated Lambda functions
4. Verify end-to-end flow

**Let me know when you have Bedrock access approved!** 🚀
