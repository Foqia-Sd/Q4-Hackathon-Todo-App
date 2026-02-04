import { authService } from './auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
const WS_URL = API_URL.replace(/^http/, 'ws') + '/realtime/ws';

type EventHandler = (data: any) => void;

class RealtimeService {
  private socket: WebSocket | null = null;
  private listeners: EventHandler[] = [];
  private reconnectTimer: any = null;

  connect() {
    const token = authService.getToken();
    if (!token) return;

    if (this.socket && (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)) {
      return;
    }

    try {
        this.socket = new WebSocket(`${WS_URL}?token=${token}`);

        this.socket.onopen = () => {
          console.log('Connected to realtime service');
        };

        this.socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.notify(data);
          } catch (e) {
            console.error('Failed to parse websocket message', e);
          }
        };

        this.socket.onclose = () => {
          console.log('Disconnected from realtime service');
          this.socket = null;
          // Reconnect after 3 seconds
          if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
          this.reconnectTimer = setTimeout(() => this.connect(), 3000);
        };

        this.socket.onerror = (error) => {
          console.error('WebSocket error:', error);
          // Only close if not already closed/closing to avoid loop logic issues
          if (this.socket && this.socket.readyState !== WebSocket.CLOSED) {
             this.socket.close();
          }
        };
    } catch (e) {
        console.error("Failed to create WebSocket:", e);
    }
  }

  disconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.socket?.close();
    this.socket = null;
  }

  subscribe(handler: EventHandler) {
    this.listeners.push(handler);
    return () => {
      this.listeners = this.listeners.filter(h => h !== handler);
    };
  }

  private notify(data: any) {
    this.listeners.forEach(handler => handler(data));
  }
}

export const realtimeService = new RealtimeService();
