import { Connection, Repository } from 'typeorm';
import { AuditEntry, AuditAction } from '../models/audit-entry';

export interface TaskEventData {
  taskId: string;
  userId: string;
  action: string;
  task: any;
  changes?: any;
}

export class AuditLogService {
  private auditRepository: Repository<AuditEntry>;

  constructor(private connection: Connection) {
    this.auditRepository = this.connection.getRepository(AuditEntry);
  }

  /**
   * Log a task event to the audit trail
   * @param eventData Event data containing task information
   */
  async logTaskEvent(eventData: TaskEventData): Promise<void> {
    try {
      const auditEntry = new AuditEntry();

      // Map the event action to audit action
      auditEntry.taskId = eventData.taskId;
      auditEntry.userId = eventData.userId;
      auditEntry.sourceService = eventData.task.source || '/services/chat-api';

      // Determine the audit action based on the event
      switch (eventData.action) {
        case 'CREATED':
        case 'com.todo.task.created':
          auditEntry.action = AuditAction.CREATED;
          auditEntry.beforeState = null;
          auditEntry.afterState = eventData.task;
          auditEntry.changedFields = 'all_fields';
          break;

        case 'UPDATED':
        case 'com.todo.task.updated':
          auditEntry.action = AuditAction.UPDATED;
          auditEntry.beforeState = eventData.changes?.previous || null;
          auditEntry.afterState = eventData.task;

          // Determine which fields were changed
          const changedFields: string[] = [];
          if (eventData.changes) {
            for (const field in eventData.changes) {
              changedFields.push(field);
            }
          }
          auditEntry.changedFields = changedFields.join(',');
          break;

        case 'COMPLETED':
        case 'com.todo.task.completed':
          auditEntry.action = AuditAction.COMPLETED;
          auditEntry.beforeState = eventData.task;
          auditEntry.afterState = { ...eventData.task, status: 'completed' };
          auditEntry.changedFields = 'status';
          break;

        case 'DELETED':
        case 'com.todo.task.deleted':
          auditEntry.action = AuditAction.DELETED;
          auditEntry.beforeState = eventData.task;
          auditEntry.afterState = null;
          auditEntry.changedFields = 'all_fields';
          break;

        default:
          console.warn(`Unknown action type: ${eventData.action}`);
          return; // Don't log unknown actions
      }

      // Save the audit entry
      await this.auditRepository.save(auditEntry);
      console.log(`Logged audit entry for task ${eventData.taskId}, action: ${auditEntry.action}`);
    } catch (error) {
      console.error('Error logging task event to audit trail:', error);
      throw error;
    }
  }
}