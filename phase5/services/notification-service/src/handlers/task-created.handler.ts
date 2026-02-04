import { ReminderService, TaskData } from '../services/reminder.service';

export class TaskCreatedHandler {
  private reminderService: ReminderService;

  constructor(reminderService: ReminderService) {
    this.reminderService = reminderService;
  }

  /**
   * Handles the TaskCreated event and schedules a reminder if applicable
   * @param cloudEvent CloudEvent containing the task creation data
   */
  async handle(cloudEvent: any): Promise<void> {
    console.log('Handling TaskCreated event:', cloudEvent);

    try {
      const eventData = cloudEvent.data;

      // Extract task data from the event
      const task = eventData.task;
      const userId = eventData.userId;

      // Check if the task has a due date
      if (!task.due_date) {
        console.log(`Task ${task.id} does not have a due date, skipping reminder scheduling`);
        return;
      }

      // Create the task data object
      const taskData: TaskData = {
        taskId: task.id,
        userId: userId,
        action: eventData.action,
        task: task
      };

      // Schedule the reminder
      await this.reminderService.scheduleReminder(taskData);

      console.log(`Reminder scheduled for new task ${task.id}`);
    } catch (error) {
      console.error('Error in TaskCreatedHandler.handle():', error);
      throw error; // Re-throw to be caught by the main event handler
    }
  }
}