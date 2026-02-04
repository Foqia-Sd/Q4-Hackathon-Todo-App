import axios from 'axios';
import { ReminderEntry } from './reminder.service';

export interface NotificationPayload {
  userId: string;
  taskId: string;
  title: string;
  message: string;
  timestamp: string;
}

export class NotificationDeliveryService {
  private chatApiUrl: string;

  constructor() {
    this.chatApiUrl = process.env.CHAT_API_URL || 'http://chat-api:8000';
  }

  /**
   * Deliver a reminder notification to the user
   * @param reminder The reminder that triggered
   */
  async deliverReminderNotification(reminder: ReminderEntry): Promise<void> {
    try {
      console.log(`Delivering reminder notification for task ${reminder.taskId}`);

      // Create notification payload
      const notificationPayload: NotificationPayload = {
        userId: reminder.userId,
        taskId: reminder.taskId,
        title: `Reminder: ${reminder.title}`,
        message: `Your task "${reminder.title}" is due soon!`,
        timestamp: new Date().toISOString()
      };

      // In a real implementation, we might:
      // 1. Send to a notification service
      // 2. Push to the user via WebSocket (using the real-time service)
      // 3. Send email/SMS

      // For now, let's simulate sending to the chat-api which could forward to WebSocket
      const response = await axios.post(
        `${this.chatApiUrl}/api/v1/notifications`,
        notificationPayload,
        {
          headers: {
            'Content-Type': 'application/json',
          },
          timeout: 10000
        }
      );

      console.log(`Notification delivered for task ${reminder.taskId}`, response.data);

      // Mark reminder as delivered in state store
      // This would require updating the reminder state to indicate it was sent
    } catch (error) {
      console.error(`Error delivering notification for task ${reminder.taskId}:`, error);
      if (axios.isAxiosError(error)) {
        console.error('Response data:', error.response?.data);
        console.error('Response status:', error.response?.status);
      }
      throw error;
    }
  }

  /**
   * Deliver a notification via WebSocket to connected users
   * @param userId The user to notify
   * @param message The notification message
   */
  async deliverViaWebSocket(userId: string, message: any): Promise<void> {
    try {
      // In a real Dapr environment, we might use a service invocation
      // to call the real-time service to send WebSocket messages
      const daprUrl = `http://localhost:${process.env.DAPR_HTTP_PORT || '3500'}/v1.0/invoke/realtime-service/method/ws-send`;

      await axios.post(daprUrl, {
        userId,
        message
      }, {
        timeout: 5000
      });

      console.log(`WebSocket notification sent to user ${userId}`);
    } catch (error) {
      console.error(`Error sending WebSocket notification to user ${userId}:`, error);
      // Fallback to other notification methods if WebSocket fails
    }
  }
}