/**
 * Core domain models
 */

export interface User {
  id: string;
  email: string;
  name?: string;
  role: 'owner' | 'admin' | 'viewer';
  createdAt: Date;
}

export interface Task {
  id: string;
  ownerId: string;
  type: string;
  status: TaskStatus;
  idempotencyKey?: string; // Prevent duplicate execution
  result?: unknown;
  error?: Error;
  createdAt: Date;
  completedAt?: Date;
}

export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

export interface WorkflowExecution {
  id: string;
  taskId: string;
  ownerId: string;
  workflowId: string;
  payload: Record<string, unknown>;
  result?: unknown;
  status: 'pending' | 'running' | 'success' | 'failed';
  startedAt: Date;
  completedAt?: Date;
  error?: string;
}
