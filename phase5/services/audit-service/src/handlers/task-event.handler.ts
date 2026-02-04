import { AuditLogService, TaskEventData } from '../services/audit-log.service';

export class TaskEventHandler {
  private auditLogService: AuditLogService;

  constructor(auditLogService: AuditLogService) {
    this.auditLogService = auditLogService;
  }

  /**
   * Handles various task events and logs them to the audit trail
   * @param cloudEvent CloudEvent containing the task event data
   */
  async handle(cloudEvent: any): Promise<void> {
    console.log('Handling task event:', cloudEvent);

    try {
      const eventData = cloudEvent.data;

      // Create a normalized task event data object
      const taskEventData: TaskEventData = {
        taskId: eventData.taskId || eventData.task?.id,
        userId: eventData.userId,
        action: cloudEvent.type || eventData.action,
        task: eventData.task,
        changes: eventData.changes || undefined
      };

      // Log the event to the audit trail
      await this.auditLogService.logTaskEvent(taskEventData);

      console.log(`Handled ${cloudEvent.type} event for task ${taskEventData.taskId}`);
    } catch (error) {
      console.error('Error in TaskEventHandler.handle():', error);
      throw error; // Re-throw to be caught by the main event handler
    }
  }
}