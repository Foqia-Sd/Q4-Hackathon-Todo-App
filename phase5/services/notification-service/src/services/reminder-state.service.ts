import axios from 'axios';
import { ReminderEntry } from './reminder.service';

export class ReminderStateService {
  private daprHttpPort: string;
  private daprGrpcPort: string;
  private stateStoreName: string;

  constructor(stateStoreName: string) {
    this.daprHttpPort = process.env.DAPR_HTTP_PORT || '3500';
    this.daprGrpcPort = process.env.DAPR_GRPC_PORT || '50001';
    this.stateStoreName = stateStoreName;
  }

  /**
   * Save a reminder to Dapr state store
   * @param reminder The reminder to save
   */
  async saveReminder(reminder: ReminderEntry): Promise<void> {
    try {
      const daprUrl = `http://localhost:${this.daprHttpPort}/v1.0/state/${this.stateStoreName}`;

      await axios.post(daprUrl, [{
        key: `reminder-${reminder.taskId}`,
        value: reminder
      }]);

      console.log(`Saved reminder for task ${reminder.taskId} to state store`);
    } catch (error) {
      console.error(`Error saving reminder for task ${reminder.taskId}:`, error);
      throw error;
    }
  }

  /**
   * Get a reminder from Dapr state store by task ID
   * @param taskId The task ID to look up
   * @returns The reminder or null if not found
   */
  async getReminder(taskId: string): Promise<ReminderEntry | null> {
    try {
      const daprUrl = `http://localhost:${this.daprHttpPort}/v1.0/state/${this.stateStoreName}/${encodeURIComponent(`reminder-${taskId}`)}`;

      const response = await axios.get(daprUrl);
      return response.data as ReminderEntry;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 404) {
        // Key not found is not an error, just return null
        return null;
      }
      console.error(`Error getting reminder for task ${taskId}:`, error);
      throw error;
    }
  }

  /**
   * Remove a reminder from Dapr state store
   * @param taskId The task ID to remove
   */
  async removeReminder(taskId: string): Promise<void> {
    try {
      const daprUrl = `http://localhost:${this.daprHttpPort}/v1.0/state/${this.stateStoreName}/${encodeURIComponent(`reminder-${taskId}`)}`;

      await axios.delete(daprUrl);
      console.log(`Removed reminder for task ${taskId} from state store`);
    } catch (error) {
      console.error(`Error removing reminder for task ${taskId}:`, error);
      throw error;
    }
  }

  /**
   * Get all reminders from state store
   * @returns Array of all reminders
   */
  async getAllReminders(): Promise<ReminderEntry[]> {
    // Note: Dapr state stores don't typically have a "get all" operation
    // In a real implementation, we might need to maintain a separate index
    // For now, we'll return an empty array and rely on other mechanisms
    // Or use a queryable state store like CosmosDB or PostgreSQL

    console.warn('getAllReminders is not fully implemented - Dapr state stores typically require querying mechanisms');
    return [];
  }

  /**
   * Bulk get reminders for specific keys
   * @param taskIds Array of task IDs to look up
   * @returns Array of reminders
   */
  async getReminders(taskIds: string[]): Promise<ReminderEntry[]> {
    try {
      const keys = taskIds.map(id => `reminder-${id}`);
      const daprUrl = `http://localhost:${this.daprHttpPort}/v1.0/state/${this.stateStoreName}/bulk`;

      const response = await axios.post(daprUrl, {
        keys: keys,
        parallelism: 10
      });

      // Filter out null/undefined responses and return valid reminders
      return response.data
        .filter((item: any) => item.data)  // Only items that exist
        .map((item: any) => item.data as ReminderEntry);
    } catch (error) {
      console.error('Error getting bulk reminders:', error);
      throw error;
    }
  }
}