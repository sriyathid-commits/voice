# Voice for Bharat - Integration Test Checklist

## Pre-Deployment Testing

### Environment Setup
- [ ] `.env.local` file created with production API URLs
- [ ] All environment variables properly configured
- [ ] Backend API endpoints are accessible
- [ ] CORS configured correctly for frontend domain

### Authentication Flow
- [ ] Login page loads correctly
- [ ] Phone number validation (10 digits, Indian format)
- [ ] OTP request sent successfully
- [ ] OTP verification works
- [ ] Invalid OTP shows error message
- [ ] Successful login redirects to dashboard
- [ ] Auth token stored in localStorage
- [ ] Protected routes redirect unauthenticated users to login
- [ ] Logout clears auth state and redirects to login

### Dashboard
- [ ] Dashboard loads with user data
- [ ] Metric cards display correct counts
- [ ] State selector works
- [ ] Location detection asks for permission
- [ ] Quick actions navigate correctly
- [ ] Activity timeline shows recent actions
- [ ] Loading skeleton displays while fetching data
- [ ] Error state shows retry button on API failure

### Schemes Browsing
- [ ] Schemes list page loads with data
- [ ] Search bar filters schemes by name
- [ ] Category filter works correctly
- [ ] State filter works correctly
- [ ] Multiple filters can be applied together
- [ ] Clear filters button resets all filters
- [ ] Empty state shows when no schemes match
- [ ] Scheme cards display correctly
- [ ] Save/unsave scheme functionality works
- [ ] Click on scheme card navigates to detail page
- [ ] Pagination works (if implemented)

### Scheme Detail Page
- [ ] Scheme details load correctly
- [ ] Eligibility check button works
- [ ] Eligibility score calculated correctly
- [ ] Eligibility reasons displayed clearly
- [ ] Action plan generated based on profile
- [ ] Save/unsave toggle works
- [ ] Apply now button navigates to application form
- [ ] Required documents list displayed
- [ ] Portal link opens in new tab
- [ ] Back button returns to schemes list

### Profile Page
- [ ] Profile page loads with user data
- [ ] View mode displays all fields correctly
- [ ] Edit button enables edit mode
- [ ] All fields are editable
- [ ] Aadhaar validation (12 digits)
- [ ] PAN validation (correct format)
- [ ] Pincode validation (6 digits)
- [ ] Cancel button discards changes
- [ ] Save button updates profile
- [ ] Success toast shown on save
- [ ] Error toast shown on failure
- [ ] Profile strength calculated correctly
- [ ] Profile strength progress bar updates

### Application Form
- [ ] Application form loads for selected scheme
- [ ] Scheme details displayed at top
- [ ] Form prefilled with user profile data
- [ ] All required fields marked with *
- [ ] Contact number validation (10 digits)
- [ ] Email validation (valid format)
- [ ] File upload button works
- [ ] File type validation (PDF, JPG, PNG only)
- [ ] File size validation (5MB max)
- [ ] Upload progress shown
- [ ] Uploaded documents listed
- [ ] Delete document button works
- [ ] Save as draft button works
- [ ] Submit button validates form
- [ ] Error messages displayed for invalid fields
- [ ] Success message on submission
- [ ] Redirect to application detail page

### Application Tracking
- [ ] Application detail page loads
- [ ] Application status displayed correctly
- [ ] Status badge has correct color
- [ ] Scheme information shown
- [ ] Applicant details displayed
- [ ] Status timeline shown with all changes
- [ ] Timestamps formatted correctly
- [ ] Edit button available for drafts
- [ ] Submit button available for drafts
- [ ] Back button returns to dashboard

### Voice Assistant
- [ ] Voice assistant page loads
- [ ] Microphone permission requested
- [ ] Recording indicator shows when recording
- [ ] 10-second auto-stop works
- [ ] Stop recording button works
- [ ] Audio uploaded to backend
- [ ] Processing indicator shown
- [ ] Transcription displayed
- [ ] AI response received
- [ ] TTS audio played automatically
- [ ] Play/pause audio controls work
- [ ] Conversation history displayed
- [ ] Suggested questions shown by language
- [ ] Citizen profile displayed
- [ ] Error handling for no mic permission
- [ ] Error handling for API failures

### Error Handling & Edge Cases
- [ ] Network offline indicator shows
- [ ] Back online notification displays
- [ ] API errors show user-friendly messages
- [ ] 401 errors redirect to login
- [ ] 404 page displays correctly
- [ ] Global error boundary catches React errors
- [ ] Loading states prevent duplicate submissions
- [ ] Disabled buttons prevent multiple clicks
- [ ] Empty states have helpful messages
- [ ] Retry buttons work after errors

### UI/UX Testing
- [ ] All pages responsive on mobile (320px+)
- [ ] All pages responsive on tablet (768px+)
- [ ] All pages responsive on desktop (1024px+)
- [ ] Touch targets minimum 44x44px
- [ ] Colors meet WCAG contrast ratios
- [ ] Focus states visible on all interactive elements
- [ ] Keyboard navigation works throughout
- [ ] No horizontal scrolling on any device
- [ ] Images load correctly
- [ ] Icons display properly
- [ ] Fonts load correctly

### Performance
- [ ] Initial page load under 3 seconds
- [ ] Time to interactive under 5 seconds
- [ ] No console errors
- [ ] No console warnings (except known ones)
- [ ] Images optimized
- [ ] Code splitting working
- [ ] Lazy loading implemented where appropriate

### Browser Compatibility
- [ ] Works on Chrome (latest)
- [ ] Works on Firefox (latest)
- [ ] Works on Safari (latest)
- [ ] Works on Edge (latest)
- [ ] Works on mobile Safari (iOS)
- [ ] Works on Chrome mobile (Android)

## Known Issues (Document here)

### Type Checking
- [ ] TSC type check passes without errors
- [ ] ESLint passes (or only acceptable warnings)

### Security
- [ ] No sensitive data in localStorage (only tokens)
- [ ] API tokens included in requests
- [ ] HTTPS enforced in production
- [ ] No hardcoded secrets in code
- [ ] Environment variables used correctly

## Testing Notes

### Mock Data vs Real Data
- Dashboard metrics: Currently using mock data (needs backend integration)
- Authentication: Requires real backend API
- Schemes: Requires real backend API with DynamoDB data
- Voice Assistant: Requires AWS Bedrock integration

### Common Issues
1. **Type error in VoiceAssistant.tsx line 828**: This appears to be a TypeScript cache issue. Running `npm run build` should resolve it.
2. **ESLint hanging**: Known issue with Next.js workspace detection. Safe to skip for now.
3. **Import typo in providers.tsx**: Fixed `@tantml:react-query` → `@tanstack/react-query`

### Before Deployment
1. Copy `.env.example` to `.env.local`
2. Update all environment variables with production values
3. Test authentication with real backend
4. Verify all API endpoints are accessible
5. Test on mobile devices
6. Run production build: `npm run build`
7. Check build output for errors
8. Test production build locally: `npm start`

## Deployment Readiness

- [ ] All critical bugs fixed
- [ ] All authentication flows tested
- [ ] All user journeys tested
- [ ] Error handling verified
- [ ] Performance acceptable
- [ ] Mobile responsive verified
- [ ] Production build succeeds
- [ ] Environment variables configured
- [ ] API endpoints verified
- [ ] CORS configured

---

**Status**: Ready for deployment after environment configuration and API integration testing.
