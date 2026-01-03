import apiClient from '../lib/api-client';

export const authService = {
  async signup(data: any) {
    const response = await apiClient.post('/auth/signup', data);
    return response.data;
  },

  async login(credentials: FormData) {
    const response = await apiClient.post('/auth/login', credentials, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  },

  logout() {
    localStorage.removeItem('token');
  },

  getToken() {
    return localStorage.getItem('token');
  },
};
