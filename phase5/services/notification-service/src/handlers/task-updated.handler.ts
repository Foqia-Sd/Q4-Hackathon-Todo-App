import { ReminderService, TaskData } from '../services/reminder.service';

export class TaskUpdatedHandler {
  private reminderService: ReminderService;

  constructor(reminderService: ReminderService) {
    this.reminderService = reminderService;
  }

  /**
   * Handles the TaskUpdated event and reschedules a reminder if applicable
   * @param cloudEvent CloudEvent containing the task update data
   */
  async handle(cloudEvent: any): Promise<void> {
    console.log('Handling TaskUpdated event:', cloudEvent);

    try {
      const eventData = cloudEvent.data;

      // Extract task data from the event
      const task = eventData.task;
      const userId = eventData.userId;

      // Check if the task has a due date
      if (!task.due_date) {
        // If the task no longer has a due date, cancel the reminder
        await this.reminderService.cancelReminder(task.id);
        console.log(`Task ${task.id} no longer has a due date, reminder cancelled`);
        return;
      }

      // Create the task data object
      const taskData: TaskData = {
        taskId: task.id,
        userId: userId,
        action: eventData.action,
        task: task
      };

      // Reschedule the reminder with updated data
      await this.reminderService.rescheduleReminder(taskData);

      console.log(`Reminder rescheduled for updated task ${task.id}`);
    } catch (error) {
      console.error('Error in TaskUpdatedHandler.handle():', error);
      throw error; // Re-throw to be caught by the main event handler
    }
  }
}