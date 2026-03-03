# After Upload - Testing Guide

## Once You Upload the AI Lambda...

### Test 1: Voice Assistant (English)
1. Go to: https://bharatvisionxai.vercel.app/assistant
2. Select "English" from dropdown
3. Click microphone
4. Say: "What schemes are available for farmers?"
5. **Expected:** Real transcription + AI response about farmer schemes

### Test 2: Voice Assistant (Hindi)
1. Select "Hindi (हिंदी)" from dropdown
2. Click microphone
3. Say: "मुझे राशन कार्ड चाहिए" (I need a ration card)
4. **Expected:** Hindi transcription + Hindi AI response + Audio playback

### Test 3: Other Languages
Try Tamil, Telugu, Marathi, or Kannada
- **Expected:** Text transcription + AI response (no audio for these languages)

### Test 4: Check CloudWatch Logs
1. Go to: https://ap-south-1.console.aws.amazon.com/cloudwatch/home?region=ap-south-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Fvoice-for-bharat-voice-service-dev
2. Click latest log stream
3. **Expected:** See Transcribe, Bedrock, Polly API calls

## Troubleshooting

### If Voice Still Shows Test Response:
- Wait 30 seconds for Lambda to update
- Hard refresh browser (Ctrl+Shift+R)
- Try again

### If You Get Errors:
- Check CloudWatch Logs for details
- Verify Bedrock access: https://ap-south-1.console.aws.amazon.com/bedrock/home?region=ap-south-1#/overview
- Check IAM permissions in Lambda

### If Transcription Fails:
- Speak clearly for 2-3 seconds
- Ensure microphone is working
- Try different browser if needed

## Success Indicators

✅ You see your actual words transcribed
✅ AI response is relevant to your question
✅ Audio plays for Hindi/English
✅ Different languages work correctly
✅ No error messages

## Performance

- First request: 5-10 seconds (cold start)
- Subsequent requests: 2-3 seconds
- Transcription: 1-2 seconds
- AI response: 1-2 seconds
- TTS generation: 1 second

## Next Steps After Testing

1. ✅ Verify all features work
2. ✅ Test on mobile device
3. ✅ Share demo link
4. ✅ Check AWS costs
5. ✅ Add more scheme data (optional)
6. ✅ Connect real DynamoDB data (optional)

## Demo Ready!

Once testing passes, your Voice for Bharat platform is fully functional and ready to demo!
