/**
 * Shared API request/response types
 */

// Authentication
export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  refreshToken?: string;
  expiresIn: number;
  owner: OwnerIdentity;
}

export interface OwnerIdentity {
  id: string;
  email: string;
  name?: string;
}

// Chat / Athena
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  metadata?: Record<string, unknown>;
}

export interface Conversation {
  id: string;
  ownerId: string;
  title?: string;
  messages: ChatMessage[];
  createdAt: Date;
  updatedAt: Date;
}

export interface ChatRequest {
  conversationId: string;
  message: string;
  idempotencyKey?: string;
}

export interface ChatResponse {
  id: string;
  conversationId: string;
  message: ChatMessage;
  context?: string;
}

// Agents
export type AgentName =
  | 'Athena'
  | 'Metis'
  | 'Hermes'
  | 'Apollo'
  | 'Themis'
  | 'Iris'
  | 'Hestia'
  | 'Prometheus'
  | 'Hecate'
  | 'Hephaestus'
  | 'Dionysus';

export interface Agent {
  id: string;
  name: AgentName;
  role: string;
  capabilities: string[];
  description: string;
  enabled: boolean;
  config?: Record<string, unknown>;
  status: AgentStatus;
  lastActivity?: Date;
}

export interface AgentStatus {
  state: 'idle' | 'busy' | 'error';
  currentTask?: string;
  message?: string;
  updatedAt: Date;
}

// Work Requests
export interface WorkRequest {
  id: string;
  type: 'linkedin' | 'jeep' | 'general';
  ownerId: string;
  title: string;
  description: string;
  status: 'draft' | 'submitted' | 'approved' | 'in_progress' | 'completed' | 'rejected';
  metadata?: Record<string, unknown>;
  createdAt: Date;
  updatedAt: Date;
}

// Approvals
export interface ApprovalItem {
  id: string;
  ownerId: string;
  taskId: string;
  workRequestId?: string;
  title: string;
  description: string;
  content: unknown;
  status: 'pending' | 'approved' | 'revised' | 'rejected';
  requiredApprovers: string[];
  approvals: Approval[];
  createdAt: Date;
  expiresAt?: Date;
}

export interface Approval {
  id: string;
  approverId: string;
  approvalItemId: string;
  status: 'approved' | 'revised' | 'rejected';
  comments?: string;
  timestamp: Date;
}

// Activity & Audit
export interface ActivityEvent {
  id: string;
  ownerId: string;
  type: string;
  action: string;
  actor?: string;
  subject: string;
  details: Record<string, unknown>;
  outcome: 'success' | 'failure' | 'pending';
  message?: string;
  timestamp: Date;
}

export interface AuditTrail {
  taskId: string;
  events: ActivityEvent[];
  summary?: string;
}

// Memory
export interface MemoryEntry {
  id: string;
  ownerId: string;
  category: string;
  key: string;
  value: unknown;
  provenance?: string; // Where this came from
  verified: boolean;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
  editedBy?: string;
}

// Settings
export interface Settings {
  ownerId: string;
  modelConfig: {
    provider: string;
    model: string;
    temperature?: number;
    maxTokens?: number;
  };
  voiceConfig: {
    enabled: boolean;
    voice?: string;
    language?: string;
  };
  permissionConfig: {
    allowWorkflowExecution: boolean;
    allowPublishing: boolean;
    allowMessaging: boolean;
  };
  integrationStatus: IntegrationStatus;
}

export interface IntegrationStatus {
  supabase: ConnectionStatus;
  n8n: ConnectionStatus;
  aiProvider: ConnectionStatus;
  timestamp: Date;
}

export interface ConnectionStatus {
  connected: boolean;
  lastChecked: Date;
  error?: string;
}

// Error Response
export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
    timestamp: Date;
  };
}
