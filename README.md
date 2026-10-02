# Athena Dashboard

A secure, portable personal dashboard connecting to n8n orchestration, AI brain, and persistent memory. Built with TypeScript, React, and Express.

## Objective

Provide Sebastian Nohse with a unified interface to:
- Chat with Athena (chief of staff AI assistant)
- Manage agents and their capabilities
- Review and approve work requests
- Track activity and audit logs
- Control memory and preferences
- Monitor integration health

All operational agents start idle. No autonomous background tasks, posting, or messaging without explicit owner approval.

## Architecture

```
┌─────────────────┐
│  React Frontend │ (iPhone-compatible, Vite)
├─────────────────┤
│   Express API   │ (TypeScript, auth middleware)
├─────────────────┤
│  Adapters       │
├────────┬────────┬────────────┤
│ Brain  │ Memory │ Orchestr.  │
│(OpenAI)│(Supabase) │(n8n)     │
└────────┴────────┴────────────┘
```

### Key Design Decisions

1. **Secrets server-side only** – No API keys, credentials, or webhooks in browser code
2. **Owner-scoped on every request** – Authentication verified server-side; owner identity not trusted from client
3. **Explicit workflow activation** – No silent triggers; scope and consequences shown before execution
4. **Idempotency and task tracking** – Duplicate submissions prevented; no ambiguous retries
5. **Honest error handling** – Real failures reported; no fake "LIVE" badges or mock activity
6. **Adapter pattern** – Brain, memory, orchestration dependencies encapsulated; portable if provider changes

## Local Setup

### Prerequisites

- Node.js 18+
- npm 9+
- git

### Installation

```bash
git clone https://github.com/sebcanzo-ctrl/Athena.git
cd Athena
npm install
```

### Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in `.env` with your actual values:
   - **JWT_SECRET**: Generate a random 32+ character string
   - **OWNER_ID** and **OWNER_EMAIL**: Your identity (verified on every protected request)
   - **Supabase**: Service role key and URL
   - **n8n**: Base URL and API key
   - **AI_API_KEY**: OpenAI or compatible provider

3. **Never commit `.env`** to version control

### Development

```bash
# Start both server and client with hot reload
npm run dev

# Or run separately
npm run dev:server  # Port 3001
npm run dev:client  # Port 5173 with proxy to /api
```

Open http://localhost:5173 in your browser.

### Typecheck and Lint

```bash
npm run typecheck
npm run lint
```

### Testing

```bash
# Watch mode
npm test

# Run once
npm run test:run
```

### Build for Production

```bash
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── client/               # React frontend
│   ├── App.tsx          # Root component
│   ├── pages/           # Screen components
│   │   ├── Login.tsx
│   │   ├── Overview.tsx
│   │   ├── Chat.tsx
│   │   ├── Agents.tsx
│   │   ├── Approvals.tsx
│   │   ├── Memory.tsx
│   │   ├── Activity.tsx
│   │   └── Settings.tsx
│   ├── components/      # Reusable UI components
│   ├── hooks/           # Custom React hooks
│   ├── api/             # API client methods
│   ├── types/           # TypeScript interfaces
│   └── main.tsx         # Entry point
├── server/              # Express backend
│   ├── index.ts         # Server initialization
│   ├── auth/            # JWT & owner verification
│   ├── routes/          # API endpoints
│   │   ├── auth.ts
│   │   ├── chat.ts
│   │   ├── agents.ts
│   │   ├── approvals.ts
│   │   ├── activity.ts
│   │   ├── memory.ts
│   │   └── settings.ts
│   ├── adapters/        # External service integrations
│   │   ├── brain.ts     # AI provider (OpenAI)
│   │   ├── memory.ts    # Supabase storage
│   │   ├── orchestrator.ts  # n8n workflows
│   │   └── types.ts     # Adapter interfaces
│   ├── middleware/      # Express middleware
│   ├── utils/           # Helpers
│   └── tests/           # Server unit tests
└── types/               # Shared TypeScript interfaces
    ├── api.ts
    ├── domain.ts
    └── errors.ts
```

## API Endpoints

### Authentication
- `POST /auth/login` – Authenticate and receive JWT
- `POST /auth/refresh` – Refresh token
- `POST /auth/logout` – Revoke session

### Chat (Athena)
- `GET /athena/conversations` – List conversation history
- `GET /athena/conversations/:id` – Get single conversation
- `POST /athena/chat` – Send message, receive reply
- `DELETE /athena/conversations/:id` – Delete conversation

### Agents
- `GET /agents` – List all agents (Metis, Hermes, Apollo, etc.)
- `GET /agents/:id` – Get agent details
- `PATCH /agents/:id` – Update agent config (owner only)
- `GET /agents/:id/status` – Real execution status

### Work Requests
- `GET /work-requests` – List all requests
- `POST /work-requests/linkedin` – Create LinkedIn content request
- `POST /work-requests/jeep` – Create Jeep/off-road request
- `PATCH /work-requests/:id` – Update request status

### Approvals
- `GET /approvals` – Pending approval queue
- `GET /approvals/:id` – Single approval detail
- `POST /approvals/:id/approve` – Approve with audit trail
- `POST /approvals/:id/revise` – Return for revision
- `POST /approvals/:id/reject` – Reject with reason

### Activity & Audit
- `GET /activity` – Event log with timestamps and outcomes
- `GET /activity/audit/:taskId` – Task-specific audit trail

### Memory
- `GET /memory` – Owner-scoped preferences and context
- `POST /memory` – Add memory entry
- `PATCH /memory/:id` – Correct memory entry
- `DELETE /memory/:id` – Remove memory (with audit)
- `POST /memory/export` – Export as JSON

### Settings
- `GET /settings` – Integration status, configuration readiness
- `GET /settings/health` – Supabase, n8n, AI provider connectivity
- `PATCH /settings` – Update model, voice, permissions

## Integration Status

### Verified
- Express.js server foundation with middleware
- JWT authentication and owner verification
- TypeScript strict mode throughout
- React frontend structure with routing
- Adapter pattern for external services

### Unverified (Requires Configuration)
- Supabase connection and RLS policy enforcement
- OpenAI/AI provider model access
- n8n workflow endpoint and API key
- Blink backend compatibility (if reusing)

### Missing (Awaiting Owner Input)
- Existing Supabase tables and schema
- Configured n8n workflows (content approval, publishing)
- AI brain endpoint and authentication
- Athena behaviour document (tone, constraints)
- Owner identity verification method

## Security Notes

1. **All secrets are server-side** – `.env` is never sent to the browser
2. **Owner scope verified on every protected request** – Client-submitted email or role not trusted
3. **Rate limiting and timeouts** – Prevent abuse and resource exhaustion
4. **Bounded requests** – All inputs validated and size-limited
5. **Idempotency tokens** – Duplicate workflow executions prevented
6. **Audit trail** – All approvals, memory edits, and sensitive actions logged
7. **No auto-retry for ambiguous actions** – Failures reported honestly
8. **Action-locking on external publishing** – No autonomous posting, messaging, or purchases

## Deployment Checklist

- [ ] `.env` configured with real credentials (not committed)
- [ ] Supabase tables created and RLS policies verified
- [ ] n8n workflows tested in sandbox environment
- [ ] AI provider API key validated
- [ ] SSL/HTTPS enabled in production
- [ ] CORS configured for frontend domain
- [ ] Rate limiting and request size limits set
- [ ] Audit logging enabled
- [ ] Backup strategy for Supabase data
- [ ] Health check endpoints monitored

## Voice and iPhone Support

- **Responsive design** – Works in iPhone Safari
- **Web app installable** – PWA manifest included
- **Voice input** (after text chat verified):
  - Explicit Start/Stop controls
  - Listening indicator
  - Transcript review before Send
  - No auto-execution
  - User-controlled playback

## Testing Strategy

### Unauthenticated Access
```bash
GET /athena/conversations
# Expected: 401 Unauthorized
```

### Non-Owner Denial
```bash
# JWT with different OWNER_ID
GET /athena/conversations
# Expected: 403 Forbidden
```

### Provider Failure Handling
- AI provider timeout → Honest error message
- Supabase connection lost → Fallback to cache; queue updates
- n8n webhook failure → Task marked failed; audit logged

### Idempotency
```bash
POST /athena/chat
Body: { conversationId, message, idempotencyKey }
# Same idempotencyKey submitted twice → Second returns cached response
```

## Known Blockers

1. **Existing Supabase schema unknown** – Awaiting table DDL and RLS policies
2. **n8n workflow URLs not provided** – Awaiting "Social JARVIS — Content Approval Spine v1" export
3. **AI brain endpoint unverified** – Assuming OpenAI; may need adjustment if using Blink's internal model
4. **Owner authentication method unclear** – Using JWT for now; can switch if existing system differs
5. **iPhone hardware testing pending** – Responsive design in place; final validation needed

## Next Steps

1. **Provide Supabase schema** → Implement memory adapter
2. **Provide n8n workflow export** → Implement orchestrator adapter
3. **Verify AI provider** → Test real Athena replies
4. **Run through all screens locally** → Capture and refine UX
5. **Test unauthenticated and non-owner denial** → Verify security
6. **Deploy to staging** → Health checks and audit logging
7. **iPhone acceptance testing** → Voice, responsive, web-app install
8. **Production release** → No public URL change, no production workflows triggered

## Cost and Dependencies

### Free Tier
- Supabase: 500 MB storage, 2 GB bandwidth included
- n8n: Self-hosted or cloud free tier (limited executions)
- OpenAI: Pay per token (estimate $0.01–$1.00 per conversation)

### No Invented Charges
- No new subscriptions created automatically
- No model swaps without explicit approval
- All provider costs are pass-through (existing)

## Contact

Owner: Sebastian Nohse
Repository: https://github.com/sebcanzo-ctrl/Athena
