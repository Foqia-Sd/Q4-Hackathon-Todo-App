import apiClient from '../lib/api-client';

interface SignupData {
  email: string;
  password: string;
  full_name?: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const authService = {
  async signup(data: SignupData): Promise<LoginResponse> {
    const response = await apiClient.post('/auth/signup', data);
    return response.data;
  },

  async login(credentials: FormData): Promise<LoginResponse> {
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

  logout(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  },

  getToken(): string | null {
    return typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  },

  getUser(): { id: string; email: string; name?: string } | null {
    if (typeof window === 'undefined') return null;
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        return JSON.parse(userStr);
      } catch {
        return null;
      }
    }
    return null;
  },

  setUser(user: { id: string; email: string; name?: string }): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('user', JSON.stringify(user));
    }
  },
};
