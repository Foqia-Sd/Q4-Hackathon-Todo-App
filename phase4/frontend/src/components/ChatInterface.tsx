'use client';

import React, { useState, useEffect, useRef, KeyboardEvent } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';

interface Message {
  id: number;
  text: string;
  sender: 'ai' | 'user';
  timestamp: Date;
  intent?: string;
}

interface ChatResponse {
  response: string;
  intent: string;
  taskId?: string | null;
  sessionId?: string | null;
  taskOperationResult?: {
    success: boolean;
    message?: string;
    tasks?: Array<{ id: string; title: string; status: string; priority: string }>;
    task?: { id: string; title: string; status: string; priority: string };
  };
  suggestions?: string[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const initialMessage: Message = {
    id: 1,
    text: "Hello! I'm your AI assistant. You can manage your tasks using natural language. Try saying something like 'Add a task to buy groceries' or 'Show me my tasks'.",
    sender: 'ai',
    timestamp: new Date()
  };

  useEffect(() => {
    // Load chat history on mount
    loadChatHistory();
  }, []);

  const loadChatHistory = async () => {
    try {
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
      if (!token) return;

      const response = await fetch(`${API_URL}/chat/history?limit=50`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const history = await response.json();
        if (history && history.length > 0) {
          const loadedMessages: Message[] = history.map((msg: { id: string; content: string; message_type: string; timestamp: string }, index: number) => ({
            id: index + 1,
            text: msg.content,
            sender: msg.message_type === 'user_input' ? 'user' : 'ai',
            timestamp: new Date(msg.timestamp)
          })).reverse();
          setMessages(loadedMessages);
        } else {
          setMessages([initialMessage]);
        }
      } else {
        setMessages([initialMessage]);
      }
    } catch (error) {
      console.error('Failed to load chat history:', error);
      setMessages([initialMessage]);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: messages.length + 1,
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

      const response = await fetch(`${API_URL}/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: inputValue,
          includeHistory: false,
          historyCount: 5
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      let responseText = data.response;

      // If viewing tasks, format them nicely
      if (data.taskOperationResult?.tasks && data.taskOperationResult.tasks.length > 0) {
        const taskList = data.taskOperationResult.tasks
          .map((task, index) => `${index + 1}. ${task.title} (${task.status}, ${task.priority})`)
          .join('\n');
        responseText = `${data.response}\n\n${taskList}`;
      }

      const aiMessage: Message = {
        id: messages.length + 2,
        text: responseText,
        sender: 'ai',
        timestamp: new Date(),
        intent: data.intent
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        id: messages.length + 2,
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] bg-white dark:bg-gray-800 rounded-xl shadow-lg border-2 border-blue-100 dark:border-blue-900/30 overflow-hidden transition-all duration-300">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-700 dark:to-gray-700/50 px-6 py-4 border-b-2 border-blue-100 dark:border-blue-900/30">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
          <Bot className="w-6 h-6 text-blue-600 dark:text-blue-400" />
          AI Task Assistant
        </h2>
        <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
          Manage your tasks using natural language
        </p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'ai' ? 'justify-start' : 'justify-end'}`}
          >
            <div className={`flex items-start gap-3 max-w-[85%] md:max-w-[75%]`}>
              {message.sender === 'ai' && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 dark:bg-blue-500 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white" />
                </div>
              )}
              <div
                className={`px-4 py-3 rounded-2xl ${
                  message.sender === 'ai'
                    ? 'bg-blue-50 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-tl-none'
                    : 'bg-blue-600 dark:bg-blue-500 text-white rounded-tr-none'
                }`}
              >
                <p className="text-sm md:text-base whitespace-pre-wrap">{message.text}</p>
                <p className={`text-xs mt-2 ${
                  message.sender === 'ai'
                    ? 'text-gray-500 dark:text-gray-400'
                    : 'text-blue-200 dark:text-blue-200'
                }`}>
                  {formatTime(message.timestamp)}
                </p>
              </div>
              {message.sender === 'user' && (
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-600 dark:bg-green-500 flex items-center justify-center">
                  <User className="w-5 h-5 text-white" />
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex items-start gap-3 max-w-[85%] md:max-w-[75%]">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 dark:bg-blue-500 flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="px-4 py-3 rounded-2xl bg-blue-50 dark:bg-gray-700 rounded-tl-none">
                <Loader2 className="w-5 h-5 text-blue-600 dark:text-blue-400 animate-spin" />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t-2 border-blue-100 dark:border-blue-900/30 p-4 bg-gray-50 dark:bg-gray-700/50">
        <div className="flex gap-3">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Type your message here..."
            disabled={isLoading}
            rows={1}
            className="flex-1 px-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400 focus:border-blue-500 dark:focus:border-blue-400 focus:ring-4 focus:ring-blue-100 dark:focus:ring-blue-900/30 outline-none transition-all duration-200 resize-none disabled:opacity-50"
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputValue.trim()}
            className="px-4 py-3 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-xl shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:hover:shadow-md"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
          Try: &quot;Add task buy groceries&quot;, &quot;Show my tasks&quot;, &quot;Complete task&quot;, &quot;Delete task&quot;
        </p>
      </div>
    </div>
  );
};

export default ChatInterface;
