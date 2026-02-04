import axios from 'axios';

export class TaskCreatorService {
  private chatApiUrl: string;

  constructor(chatApiUrl: string) {
    this.chatApiUrl = chatApiUrl;
  }

  /**
   * Creates a new task via the Chat API
   * @param taskData Task data to create
   * @param userId User ID for the task
   * @returns Created task or null if failed
   */
  async createTask(taskData: any, userId: string): Promise<any | null> {
    try {
      console.log(`Creating new task via Chat API: ${this.chatApiUrl}/api/tasks`);

      // Prepare headers with user context
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.USER_TOKEN || 'mock-token'}`, // In real scenario, you'd have proper auth
      };

      // Call the Chat API to create the new recurring task
      const response = await axios.post(
        `${this.chatApiUrl}/api/v1/tasks`,
        {
          ...taskData,
          user_id: userId // Ensure the user ID is properly set
        },
        {
          headers,
          timeout: 10000 // 10 second timeout
        }
      );

      console.log('Successfully created new recurring task:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error creating task via Chat API:', error);
      if (axios.isAxiosError(error)) {
        console.error('Response data:', error.response?.data);
        console.error('Response status:', error.response?.status);
        console.error('Response headers:', error.response?.headers);
      }
      return null;
    }
  }
}