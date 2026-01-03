import apiClient from '../lib/api-client';

export const taskService = {
  async getTasks(filters?: { status?: string; priority?: string; category?: string; search?: string }) {
    const response = await apiClient.get('/tasks/', { params: filters });
    return response.data;
  },

  async createTask(task: { title: string; priority?: string; category?: string }) {
    const response = await apiClient.post('/tasks/', task);
    return response.data;
  },

  async updateTask(id: string, updates: any) {
    const response = await apiClient.put(`/tasks/${id}`, updates);
    return response.data;
  },

  async deleteTask(id: string) {
    const response = await apiClient.delete(`/tasks/${id}`);
    return response.data;
  },
};
