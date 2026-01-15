'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { taskService } from '@/services/tasks';
import { authService } from '@/services/auth';

export default function CompletedTasksPage() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
  const router = useRouter();

  useEffect(() => {
    const token = authService.getToken();
    if (!token) {
      router.push('/auth/login');
      return;
    }
    fetchCompletedTasks();
  }, []);

  const showToast = (message: string, type: 'success' | 'error') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  const fetchCompletedTasks = async () => {
    try {
      const allTasks = await taskService.getTasks();
      const completedTasks = allTasks.filter(task => task.status === 'completed');
      setTasks(completedTasks);
    } catch (err) {
      console.error('Failed to fetch completed tasks', err);
      showToast('Failed to fetch completed tasks', 'error');
    } finally {
      setLoading(false);
    }
  };

  const toggleStatus = async (task: any) => {
    try {
      const newStatus = task.status === 'pending' ? 'completed' : 'pending';
      await taskService.updateTask(task.id, { status: newStatus });
      fetchCompletedTasks(); // Refresh the list
      showToast(`Task marked as ${newStatus}!`, 'success');
    } catch (err) {
      console.error('Failed to update status', err);
      showToast('Failed to update task', 'error');
    }
  };

  const deleteTask = async (id: string) => {
    try {
      await taskService.deleteTask(id);
      fetchCompletedTasks(); // Refresh the list
      showToast('Task deleted successfully!', 'success');
    } catch (err) {
      console.error('Failed to delete task', err);
      showToast('Failed to delete task', 'error');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-4 md:p-8 transition-colors duration-300">
      <div className="max-w-4xl mx-auto">
        {/* Toast Notification */}
        {toast && (
          <div className={`fixed top-4 right-4 z-50 px-6 py-4 rounded-xl shadow-2xl animate-fade-in backdrop-blur-sm ${
            toast.type === 'success'
              ? 'bg-green-600 text-white dark:bg-green-500'
              : 'bg-red-600 text-white dark:bg-red-500'
          }`}>
            <div className="flex items-center gap-2">
              <span className="text-lg">{toast.type === 'success' ? '✓' : '✕'}</span>
              <span className="font-medium">{toast.message}</span>
            </div>
          </div>
        )}

        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Completed Tasks</h1>
          <p className="text-gray-600 dark:text-gray-300 mt-2">
            Tasks you have marked as completed
          </p>
        </div>

        {loading ? (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border-2 border-gray-200 dark:border-gray-700 p-16 transition-all duration-300">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-200 dark:border-gray-600 border-t-green-600 dark:border-t-green-400"></div>
              <p className="mt-4 text-gray-600 dark:text-gray-300 font-medium">Loading completed tasks...</p>
            </div>
          </div>
        ) : tasks.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border-2 border-gray-200 dark:border-gray-700 p-16 text-center transition-all duration-300">
            <div className="text-6xl mb-4">🎉</div>
            <p className="text-gray-600 dark:text-gray-300 text-lg">
              No completed tasks yet. Great job on staying productive!
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="group bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-xl border-l-4 border-green-500 dark:border-green-400 border-2 border-r-2 border-t-2 border-b-2 border-gray-200 dark:border-gray-700 overflow-hidden transition-all duration-300 hover:-translate-y-1"
              >
                <div className="p-5">
                  <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                    <div className="flex items-start sm:items-center gap-4 flex-1 w-full sm:w-auto">
                      <input
                        type="checkbox"
                        checked={task.status === 'completed'}
                        onChange={() => toggleStatus(task)}
                        className="w-6 h-6 rounded border-2 border-gray-300 dark:border-gray-600 text-green-600 focus:ring-4 focus:ring-green-100 dark:focus:ring-green-900/30 mt-1 sm:mt-0 flex-shrink-0 cursor-pointer transition-all duration-200"
                      />
                      <div className="flex flex-col flex-1 min-w-0">
                        <span
                          className={`text-lg font-medium break-words transition-all duration-200 ${
                            task.status === 'completed'
                              ? 'line-through text-gray-400 dark:text-gray-500'
                              : 'text-gray-900 dark:text-white'
                          }`}
                        >
                          {task.title}
                        </span>
                        <div className="flex flex-wrap gap-2 mt-3">
                          <span
                            className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide ${
                              task.priority === 'high'
                                ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
                                : task.priority === 'medium'
                                ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
                                : 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
                            }`}
                          >
                            {task.priority}
                          </span>
                          {task.category && (
                            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300 border-2 border-gray-300 dark:border-gray-600">
                              {task.category}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={() => deleteTask(task.id)}
                      className="px-4 py-2 text-sm font-semibold text-gray-600 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-all duration-200 self-end sm:self-center"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}