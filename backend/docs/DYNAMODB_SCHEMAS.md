# DynamoDB Table Schemas

This document provides comprehensive documentation for all DynamoDB tables used in the Voice for Bharat application.

## Overview

The application uses 8 DynamoDB tables with On-Demand billing mode, AWS-managed encryption (SSE), and Point-in-Time Recovery enabled for all tables.

## Table Naming Convention

All tables use the prefix pattern: `{TablePrefix}-{table-name}`

Example: `voice-for-bharat-dev-users`

## Tables

### 1. Users Table

**Table Name**: `{TablePrefix}-users`

**Purpose**: Store user authentication and profile information

**Primary Key**:
- Partition Key: `userId` (String)

**Global Secondary Indexes**:
1. **phoneNumber-index**
   - Partition Key: `phoneNumber` (String)
   - Projection: ALL
   - Purpose: Login lookup and authentication

2. **state-category-index**
   - Partition Key: `state` (String)
   - Sort Key: `category` (String)
   - Projection: ALL
   - Purpose: Analytics and user segmentation

3. **cognitoId-index**
   - Partition Key: `cognitoId` (String)
   - Projection: ALL
   - Purpose: Cognito integration and user lookup

**Key Attributes**:
- `userId` (String) - Unique user identifier (UUID)
- `phoneNumber` (String) - 10-digit Indian mobile number
- `cognitoId` (String) - AWS Cognito user ID
- `state` (String) - Indian state code
- `category` (String) - User category (General, OBC, SC, ST, etc.)
- `name` (String) - User's full name
- `dateOfBirth` (String) - ISO 8601 date format
- `gender` (String) - Gender (Male, Female, Other)
- `district` (String) - District name
- `income` (Number) - Annual income in INR
- `aadhaarNumber` (String) - Encrypted Aadhaar number
- `panNumber` (String) - Encrypted PAN number
- `bankAccountNumber` (String) - Encrypted bank account
- `savedSchemes` (List) - Array of saved scheme IDs
- `profileStrength` (Number) - Profile completion percentage (0-100)
- `createdAt` (String) - ISO 8601 timestamp
- `updatedAt` (String) - ISO 8601 timestamp
- `lastLoginAt` (String) - ISO 8601 timestamp

**Capacity**: Expected 10M users

---

### 2. Schemes Table

**Table Name**: `{TablePrefix}-schemes`

**Purpose**: Store government welfare scheme information

**Primary Key**:
- Partition Key: `schemeId` (String)

**Global Secondary Indexes**:
1. **state-category-index**
   - Partition Key: `state` (String)
   - Sort Key: `category` (String)
   - Projection: ALL
   - Purpose: Filter schemes by state and category

2. **isActive-lastSyncedAt-index**
   - Partition Key: `isActive` (String)
   - Sort Key: `lastSyncedAt` (String)
   - Projection: ALL
   - Purpose: Sync operations and active scheme queries

3. **category-viewCount-index**
   - Partition Key: `category` (String)
   - Sort Key: `viewCount` (Number)
   - Projection: ALL
   - Purpose: Popular schemes by category

**Key Attributes**:
- `schemeId` (String) - Unique scheme identifier (UUID)
- `name` (Map) - Scheme name in multiple languages {en, hi, mr, kn, ta, te}
- `description` (Map) - Scheme description in multiple languages
- `state` (String) - State code or "ALL_INDIA"
- `category` (String) - Scheme category (education, health, agriculture, pension, etc.)
- `isActive` (String) - "true" or "false" (String for GSI)
- `lastSyncedAt` (String) - ISO 8601 timestamp
- `viewCount` (Number) - Number of times scheme was viewed
- `eligibilityCriteria` (Map) - Eligibility rules (minAge, maxAge, gender, incomeLimit, categories)
- `benefits` (Map) - Benefits description in multiple languages
- `applicationProcess` (Map) - Application steps in multiple languages
- `requiredDocuments` (List) - Array of required document types
- `portalUrl` (String) - Government portal URL
- `portalStatus` (String) - ACTIVE, MAINTENANCE, OFFLINE
- `createdAt` (String) - ISO 8601 timestamp
- `updatedAt` (String) - ISO 8601 timestamp

**Capacity**: Expected 5K schemes

---

### 3. Applications Table

**Table Name**: `{TablePrefix}-applications`

**Purpose**: Store user applications to welfare schemes

**Primary Key**:
- Partition Key: `applicationId` (String)

**Global Secondary Indexes**:
1. **userId-status-index**
   - Partition Key: `userId` (String)
   - Sort Key: `status` (String)
   - Projection: ALL
   - Purpose: User's application list filtered by status

2. **schemeId-submittedAt-index**
   - Partition Key: `schemeId` (String)
   - Sort Key: `submittedAt` (String)
   - Projection: ALL
   - Purpose: Scheme analytics and application tracking

3. **status-updatedAt-index**
   - Partition Key: `status` (String)
   - Sort Key: `updatedAt` (String)
   - Projection: ALL
   - Purpose: Status-based queries and monitoring

**Key Attributes**:
- `applicationId` (String) - Unique application identifier (UUID)
- `userId` (String) - User ID reference
- `schemeId` (String) - Scheme ID reference
- `status` (String) - DRAFT, SUBMITTED, UNDER_REVIEW, APPROVED, REJECTED, WITHDRAWN
- `submittedAt` (String) - ISO 8601 timestamp
- `updatedAt` (String) - ISO 8601 timestamp
- `formData` (Map) - Application form data
- `documents` (List) - Array of document references
- `externalReferenceId` (String) - Government portal reference ID
- `statusHistory` (List) - Array of status changes with timestamps
- `notes` (String) - Application notes
- `createdAt` (String) - ISO 8601 timestamp

**Capacity**: Expected 50M applications

---

### 4. Activity Log Table

**Table Name**: `{TablePrefix}-activity-log`

**Purpose**: Store user activity tracking with automatic expiration

**Primary Key**:
- Partition Key: `activityId` (String)

**Global Secondary Indexes**:
1. **userId-timestamp-index**
   - Partition Key: `userId` (String)
   - Sort Key: `timestamp` (String)
   - Projection: ALL
   - Purpose: User activity timeline

2. **type-timestamp-index**
   - Partition Key: `type` (String)
   - Sort Key: `timestamp` (String)
   - Projection: ALL
   - Purpose: Activity type analytics

3. **schemeId-timestamp-index**
   - Partition Key: `schemeId` (String)
   - Sort Key: `timestamp` (String)
   - Projection: ALL
   - Purpose: Scheme-specific activity tracking

**TTL Configuration**:
- TTL Attribute: `ttl` (Number)
- Retention: 90 days (automatically deleted after expiration)

**Key Attributes**:
- `activityId` (String) - Unique activity identifier (UUID)
- `userId` (String) - User ID reference
- `type` (String) - Activity type (SCHEME_VIEWED, APPLICATION_STARTED, DOCUMENT_UPLOADED, etc.)
- `timestamp` (String) - ISO 8601 timestamp
- `ttl` (Number) - Unix timestamp for automatic deletion (90 days from creation)
- `schemeId` (String) - Related scheme ID (optional)
- `applicationId` (String) - Related application ID (optional)
- `metadata` (Map) - Additional activity data
- `ipAddress` (String) - User IP address
- `userAgent` (String) - User agent string

**Capacity**: High write volume, automatic cleanup via TTL

---

### 5. User Profile Table

**Table Name**: `{TablePrefix}-user-profile`

**Purpose**: Store extended user profile data for eligibility matching

**Primary Key**:
- Partition Key: `userId` (String)

**Global Secondary Indexes**:
1. **state-profileStrength-index**
   - Partition Key: `state` (String)
   - Sort Key: `profileStrength` (Number)
   - Projection: ALL
   - Purpose: Profile completion analytics by state

2. **educationLevel-annualIncome-index**
   - Partition Key: `educationLevel` (String)
   - Sort Key: `annualIncome` (Number)
   - Projection: ALL
   - Purpose: Demographic analytics and targeting

**Key Attributes**:
- `userId` (String) - User ID reference
- `state` (String) - Indian state code
- `profileStrength` (Number) - Profile completion percentage (0-100)
- `educationLevel` (String) - Education level (ILLITERATE, PRIMARY, SECONDARY, GRADUATE, POST_GRADUATE)
- `annualIncome` (Number) - Annual income in INR
- `occupation` (String) - Occupation type
- `familySize` (Number) - Number of family members
- `landOwnership` (String) - Land ownership status
- `rationCardType` (String) - BPL, APL, AAY, etc.
- `rationCardNumber` (String) - Ration card number
- `disabilityStatus` (String) - Disability status
- `maritalStatus` (String) - Marital status
- `religion` (String) - Religion
- `caste` (String) - Caste category
- `createdAt` (String) - ISO 8601 timestamp
- `updatedAt` (String) - ISO 8601 timestamp

**Capacity**: Expected 10M profiles

---

### 6. Helplines Table

**Table Name**: `{TablePrefix}-helplines`

**Purpose**: Store helpline contact information

**Primary Key**:
- Partition Key: `helplineId` (String)

**Global Secondary Indexes**:
1. **state-category-index**
   - Partition Key: `state` (String)
   - Sort Key: `category` (String)
   - Projection: ALL
   - Purpose: Filter helplines by state and category

2. **isActive-state-index**
   - Partition Key: `isActive` (String)
   - Sort Key: `state` (String)
   - Projection: ALL
   - Purpose: Active helplines by state

**Key Attributes**:
- `helplineId` (String) - Unique helpline identifier (UUID)
- `name` (Map) - Helpline name in multiple languages
- `phoneNumber` (String) - Contact phone number
- `category` (String) - Category (welfare, health, emergency, agriculture, education)
- `state` (String) - State code or "ALL_INDIA"
- `isActive` (String) - "true" or "false" (String for GSI)
- `availability` (String) - Hours of operation (e.g., "24/7", "9 AM - 6 PM")
- `languages` (List) - Supported languages
- `description` (Map) - Description in multiple languages
- `createdAt` (String) - ISO 8601 timestamp
- `updatedAt` (String) - ISO 8601 timestamp

**Capacity**: Expected 1K helplines

---

### 7. Guide Content Table

**Table Name**: `{TablePrefix}-guide-content`

**Purpose**: Store FAQ and guide content

**Primary Key**:
- Partition Key: `contentId` (String)

**Global Secondary Indexes**:
1. **category-state-priority-index**
   - Partition Key: `category` (String)
   - Sort Key: `priority` (Number)
   - Projection: ALL
   - Purpose: Quick guide queries with priority ordering

2. **state-lastUpdatedAt-index**
   - Partition Key: `state` (String)
   - Sort Key: `lastUpdatedAt` (String)
   - Projection: ALL
   - Purpose: Content management and updates

3. **category-viewCount-index**
   - Partition Key: `category` (String)
   - Sort Key: `viewCount` (Number)
   - Projection: ALL
   - Purpose: Popular content analytics

**Key Attributes**:
- `contentId` (String) - Unique content identifier (UUID)
- `category` (String) - Category (quick-guide, faq, tutorial, troubleshooting)
- `state` (String) - State code or "ALL_INDIA"
- `priority` (Number) - Priority (1-100, higher = more important)
- `question` (Map) - Question in multiple languages
- `answer` (Map) - Answer in multiple languages
- `tags` (List) - Searchable tags
- `relatedSchemes` (List) - Related scheme IDs
- `viewCount` (Number) - Number of views
- `lastUpdatedAt` (String) - ISO 8601 timestamp
- `isActive` (Boolean) - Active status
- `createdAt` (String) - ISO 8601 timestamp

**Capacity**: Expected 5K content items

---

### 8. Suggested Queries Table

**Table Name**: `{TablePrefix}-suggested-queries`

**Purpose**: Store suggested voice queries for users

**Primary Key**:
- Partition Key: `queryId` (String)

**Global Secondary Indexes**:
1. **state-displayOrder-index**
   - Partition Key: `state` (String)
   - Sort Key: `displayOrder` (Number)
   - Projection: ALL
   - Purpose: Display suggested questions in order

2. **category-popularity-index**
   - Partition Key: `category` (String)
   - Sort Key: `popularity` (Number)
   - Projection: ALL
   - Purpose: Analytics on popular queries

3. **isActive-state-index**
   - Partition Key: `isActive` (String)
   - Sort Key: `state` (String)
   - Projection: ALL
   - Purpose: Active queries by state

**Key Attributes**:
- `queryId` (String) - Unique query identifier (UUID)
- `text` (Map) - Query text in multiple languages
- `category` (String) - Category (ration-card, health, agriculture, education, pension)
- `state` (String) - State code or "ALL_INDIA"
- `isActive` (String) - "true" or "false" (String for GSI)
- `intent` (String) - Voice service intent type
- `entities` (Map) - Pre-filled entities for the query
- `popularity` (Number) - Usage count
- `displayOrder` (Number) - Display order (1-100)
- `lastUpdatedAt` (String) - ISO 8601 timestamp
- `createdAt` (String) - ISO 8601 timestamp

**Capacity**: Expected 500 suggested queries

---

## Common Configuration

All tables share the following configuration:

- **Billing Mode**: ON_DEMAND (pay-per-request)
- **Encryption**: AWS-managed SSE (Server-Side Encryption)
- **Point-in-Time Recovery**: Enabled
- **Deletion Protection**: Recommended for production
- **Tags**:
  - `Environment`: dev/staging/production
  - `Application`: voice-for-bharat

## Data Types

- **String**: Text data, timestamps (ISO 8601), UUIDs
- **Number**: Numeric values (integers, decimals)
- **Boolean**: True/false values
- **List**: Arrays of values
- **Map**: Key-value pairs (nested objects)

## Best Practices

1. **Timestamps**: Always use ISO 8601 format (e.g., "2024-01-15T10:30:00Z")
2. **UUIDs**: Use UUID v4 for all ID fields
3. **Phone Numbers**: Store as strings without formatting (e.g., "9876543210")
4. **Encryption**: Sensitive fields (Aadhaar, PAN, bank account) should be encrypted before storage
5. **TTL**: Use Unix timestamps (seconds since epoch) for TTL attributes
6. **Boolean GSI**: Use string "true"/"false" for boolean values in GSI partition keys
7. **Multilingual**: Store translations in Map with language codes as keys (en, hi, mr, kn, ta, te)

## Access Patterns

### Users Table
- Get user by ID: `GetItem(userId)`
- Login lookup: `Query(phoneNumber-index, phoneNumber)`
- Users by state and category: `Query(state-category-index, state, category)`
- Cognito integration: `Query(cognitoId-index, cognitoId)`

### Schemes Table
- Get scheme by ID: `GetItem(schemeId)`
- Schemes by state and category: `Query(state-category-index, state, category)`
- Active schemes for sync: `Query(isActive-lastSyncedAt-index, isActive="true")`
- Popular schemes: `Query(category-viewCount-index, category, ScanIndexForward=false)`

### Applications Table
- Get application by ID: `GetItem(applicationId)`
- User's applications: `Query(userId-status-index, userId)`
- Applications by status: `Query(status-updatedAt-index, status)`
- Scheme applications: `Query(schemeId-submittedAt-index, schemeId)`

### Activity Log Table
- User activity timeline: `Query(userId-timestamp-index, userId)`
- Activity by type: `Query(type-timestamp-index, type)`
- Scheme activity: `Query(schemeId-timestamp-index, schemeId)`

### User Profile Table
- Get profile by user ID: `GetItem(userId)`
- Profiles by state: `Query(state-profileStrength-index, state)`
- Demographics: `Query(educationLevel-annualIncome-index, educationLevel)`

### Helplines Table
- Get helpline by ID: `GetItem(helplineId)`
- Helplines by state and category: `Query(state-category-index, state, category)`
- Active helplines: `Query(isActive-state-index, isActive="true", state)`

### Guide Content Table
- Get content by ID: `GetItem(contentId)`
- Quick guides: `Query(category-state-priority-index, category, state)`
- Recent updates: `Query(state-lastUpdatedAt-index, state)`
- Popular content: `Query(category-viewCount-index, category)`

### Suggested Queries Table
- Get query by ID: `GetItem(queryId)`
- Display queries: `Query(state-displayOrder-index, state)`
- Popular queries: `Query(category-popularity-index, category)`
- Active queries: `Query(isActive-state-index, isActive="true", state)`

## Monitoring

Monitor the following CloudWatch metrics for each table:
- `ConsumedReadCapacityUnits`
- `ConsumedWriteCapacityUnits`
- `UserErrors`
- `SystemErrors`
- `ThrottledRequests`

## Backup Strategy

- **Point-in-Time Recovery**: Enabled for all tables (35-day retention)
- **On-Demand Backups**: Create before major deployments
- **Cross-Region Replication**: Consider for disaster recovery in production
