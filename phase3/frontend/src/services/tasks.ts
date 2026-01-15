import apiClient from '../lib/api-client';

interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'completed';
  priority: 'low' | 'medium' | 'high';
  category?: string;
  created_at: string;
  updated_at: string;
}

interface TaskFilters {
  status?: string;
  priority?: string;
  category?: string;
  search?: string;
}

interface CreateTaskData {
  title: string;
  priority?: string;
  category?: string;
  description?: string;
}

interface UpdateTaskData {
  title?: string;
  description?: string;
  status?: 'pending' | 'completed';
  priority?: 'low' | 'medium' | 'high';
  category?: string;
}

export const taskService = {
  async getTasks(filters?: TaskFilters): Promise<Task[]> {
    const response = await apiClient.get('/tasks/', { params: filters });
    return response.data;
  },

  async createTask(task: CreateTaskData): Promise<Task> {
    const response = await apiClient.post('/tasks/', task);
    return response.data;
  },

  async updateTask(id: string, updates: UpdateTaskData): Promise<Task> {
    const response = await apiClient.put(`/tasks/${id}`, updates);
    return response.data;
  },

  async deleteTask(id: string): Promise<void> {
    const response = await apiClient.delete(`/tasks/${id}`);
    return response.data;
  },
};

export type { Task, TaskFilters, CreateTaskData, UpdateTaskData };
