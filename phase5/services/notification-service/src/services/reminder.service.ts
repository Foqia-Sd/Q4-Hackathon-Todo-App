import { ReminderStateService } from './reminder-state.service';

export interface TaskData {
  taskId: string;
  userId: string;
  action: string;
  task: {
    id: string;
    title: string;
    description?: string;
    due_date?: string;
    reminder_offset?: number; // minutes before due date
    status: string;
    user_id: string;
    created_at: string;
    updated_at: string;
  };
}

export interface ReminderEntry {
  taskId: string;
  userId: string;
  dueDate: string;
  reminderTime: string;
  title: string;
  scheduled: boolean;
}

export class ReminderService {
  private reminderStateService: ReminderStateService;

  constructor(reminderStateService: ReminderStateService) {
    this.reminderStateService = reminderStateService;
  }

  /**
   * Schedule a reminder for a task based on its due date and reminder offset
   * @param taskData Task data containing due date and reminder offset
   */
  async scheduleReminder(taskData: TaskData): Promise<void> {
    const task = taskData.task;

    // Check if the task has a due date
    if (!task.due_date) {
      console.log(`Task ${task.id} has no due date, skipping reminder scheduling`);
      return;
    }

    // Calculate reminder time based on due date and offset
    const dueDate = new Date(task.due_date);
    const reminderOffset = task.reminder_offset || 15; // Default to 15 minutes before

    // Calculate when the reminder should fire
    const reminderTime = new Date(dueDate.getTime() - (reminderOffset * 60 * 1000));

    // Only schedule if the reminder time is in the future
    if (reminderTime <= new Date()) {
      console.log(`Task ${task.id} reminder time has already passed, not scheduling`);
      return;
    }

    // Create a reminder entry
    const reminderEntry: ReminderEntry = {
      taskId: task.id,
      userId: taskData.userId,
      dueDate: task.due_date,
      reminderTime: reminderTime.toISOString(),
      title: task.title,
      scheduled: true
    };

    // Save the reminder to state
    await this.reminderStateService.saveReminder(reminderEntry);
    console.log(`Scheduled reminder for task ${task.id} at ${reminderTime.toISOString()}`);
  }

  /**
   * Reschedule a reminder when a task is updated
   * @param taskData Updated task data
   */
  async rescheduleReminder(taskData: TaskData): Promise<void> {
    // Remove the old reminder
    await this.reminderStateService.removeReminder(taskData.task.id);

    // Schedule a new reminder with updated data
    await this.scheduleReminder(taskData);
  }

  /**
   * Cancel a reminder for a task (e.g., when task is completed)
   * @param taskId ID of the task
   */
  async cancelReminder(taskId: string): Promise<void> {
    await this.reminderStateService.removeReminder(taskId);
    console.log(`Cancelled reminder for task ${taskId}`);
  }

  /**
   * Get all reminders that are due now or in the past minute
   * @returns Array of due reminders
   */
  async getDueReminders(): Promise<ReminderEntry[]> {
    const allReminders = await this.reminderStateService.getAllReminders();
    const now = new Date();
    const oneMinuteAgo = new Date(now.getTime() - 60000); // 1 minute ago

    return allReminders.filter(reminder => {
      const reminderTime = new Date(reminder.reminderTime);
      return reminderTime >= oneMinuteAgo && reminderTime <= now && reminder.scheduled;
    });
  }
}