/**
 * Service for interacting with the AI chat API
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface ChatOptions {
  sessionId?: string;
  includeHistory?: boolean;
  historyCount?: number;
}

interface TaskResult {
  id: string;
  title: string;
  status: string;
  priority: string;
}

interface ChatResponse {
  response: string;
  intent: string;
  taskId?: string | null;
  sessionId?: string | null;
  taskOperationResult?: {
    success: boolean;
    message?: string;
    tasks?: TaskResult[];
    task?: TaskResult;
  };
  suggestions?: string[];
}

interface HistoryOptions {
  limit?: number;
  offset?: number;
}

interface ChatHistoryMessage {
  id: string;
  user_id: string;
  message_type: 'user_input' | 'ai_response';
  content: string;
  intent_classification?: string;
  task_operation_params?: string;
  timestamp: string;
  session_id?: string;
}

interface SessionResponse {
  sessionId: string;
}

class AIService {
  private getToken(): string | null {
    return typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  }

  /**
   * Process a user's natural language input
   */
  async processChatInput(message: string, options: ChatOptions = {}): Promise<ChatResponse> {
    const { sessionId, includeHistory = false, historyCount = 5 } = options;
    const token = this.getToken();

    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        message,
        sessionId,
        includeHistory,
        historyCount
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Get chat history for the current user
   */
  async getChatHistory(options: HistoryOptions = {}): Promise<ChatHistoryMessage[]> {
    const { limit = 50, offset = 0 } = options;
    const token = this.getToken();

    const response = await fetch(`${API_BASE_URL}/chat/history?limit=${limit}&offset=${offset}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Create a new chat session
   */
  async createSession(): Promise<SessionResponse> {
    // Generate a random session ID client-side
    return {
      sessionId: Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15)
    };
  }
}

const aiService = new AIService();
export default aiService;
export { AIService };
export type { ChatResponse, ChatOptions, ChatHistoryMessage, TaskResult };
