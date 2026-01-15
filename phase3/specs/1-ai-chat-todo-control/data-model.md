# Data Model: AI-Powered Natural Language Todo Control

## New Database Tables

### ChatMessage
- **id**: UUID (Primary Key) - Unique identifier for each chat message
- **user_id**: UUID (Foreign Key) - Links to the authenticated user
- **message_type**: String (ENUM: 'user_input', 'ai_response') - Distinguishes between user inputs and AI responses
- **content**: Text - The actual message content (user input or AI response)
- **intent_classification**: String (Optional) - The AI's interpretation of user intent ('add_task', 'view_tasks', 'complete_task', 'delete_task', 'other')
- **task_operation_params**: JSON (Optional) - Parameters extracted from user input for task operations
- **timestamp**: DateTime - When the message was created
- **session_id**: UUID (Optional) - Groups messages into conversation sessions
- **created_at**: DateTime - Record creation timestamp
- **updated_at**: DateTime - Record update timestamp

**Relationships**:
- Belongs to User (via user_id foreign key)
- Each ChatMessage is linked to a specific user for data isolation

**Indexes**:
- Index on user_id for efficient user-specific queries
- Index on session_id for efficient session retrieval
- Composite index on (user_id, timestamp) for chronological retrieval

## Updated Existing Models (No Changes Required)

### Task (Remains Unchanged)
- Existing model stays the same to preserve functionality
- AI agent will interact with existing task operations through backend skills

### User (Remains Unchanged)
- Existing model stays the same to preserve authentication
- ChatMessage links to existing user for authorization

## Validation Rules

### ChatMessage Validation
- content must be 1-2000 characters
- message_type must be one of the allowed enum values
- user_id must reference an existing user
- timestamp must be current or past (not future)

### Session Management
- Each conversation session can contain multiple ChatMessage records
- Sessions may be implicitly created based on time gaps between messages
- Sessions help maintain context for the AI agent

## State Transitions

### Message Lifecycle
1. User sends message → ChatMessage record created with message_type='user_input'
2. AI processes message → ChatMessage record created with message_type='ai_response' and intent_classification
3. Task operation executed (if applicable) → Existing Task model updated through backend skills
4. Response returned to user → ChatMessage with AI response displayed in UI

## Privacy and Security Considerations

### Data Isolation
- Chat history is strictly partitioned by user_id
- Users can only access their own chat history
- No cross-user data exposure possible

### Data Retention
- Chat history persists as long as the user account exists
- Future enhancements may include configurable retention periods
- All chat data follows the same backup and archival procedures as other user data

## Performance Considerations

### Query Patterns
- Retrieve recent chat history for a user: SELECT with user_id and descending timestamp ordering
- Retrieve chat history for a session: SELECT with session_id
- Pagination support for long conversations: LIMIT and OFFSET clauses

### Indexing Strategy
- Primary indexes ensure fast lookups for user-specific data
- Composite indexes support efficient chronological retrieval
- Foreign key constraints maintain referential integrity