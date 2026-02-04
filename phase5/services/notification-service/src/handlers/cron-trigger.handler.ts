import { ReminderService } from '../services/reminder.service';
import { NotificationDeliveryService } from '../services/notification-delivery.service';

export class CronTriggerHandler {
  private reminderService: ReminderService;
  private notificationDeliveryService: NotificationDeliveryService;

  constructor(
    reminderService: ReminderService,
    notificationDeliveryService: NotificationDeliveryService
  ) {
    this.reminderService = reminderService;
    this.notificationDeliveryService = notificationDeliveryService;
  }

  /**
   * Handles the cron-trigger event and delivers due reminders
   */
  async handle(): Promise<void> {
    console.log('Checking for due reminders...');

    try {
      // Get all reminders that are due now
      const dueReminders = await this.reminderService.getDueReminders();

      if (dueReminders.length === 0) {
        console.log('No due reminders found');
        return;
      }

      console.log(`Found ${dueReminders.length} due reminders`);

      // Process each due reminder
      for (const reminder of dueReminders) {
        try {
          // Deliver the notification
          await this.notificationDeliveryService.deliverReminderNotification(reminder);

          // Cancel the reminder since it's been delivered
          await this.reminderService.cancelReminder(reminder.taskId);
        } catch (error) {
          console.error(`Error processing reminder for task ${reminder.taskId}:`, error);
          // Continue with other reminders even if one fails
        }
      }
    } catch (error) {
      console.error('Error in CronTriggerHandler.handle():', error);
      throw error;
    }
  }
}