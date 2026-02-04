'use client';

import { useState, useEffect } from 'react';
import { taskService } from '@/services/tasks';
import { authService } from '@/services/auth';
import { realtimeService } from '@/services/realtime';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<any[]>([]);
  const [newTask, setNewTask] = useState('');
  const [priority, setPriority] = useState('medium');
  const [category, setCategory] = useState('');
  const [loading, setLoading] = useState(true);

  // Filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [filterPriority, setFilterPriority] = useState('');
  const [filterCategory, setFilterCategory] = useState('');
  const [sortBy, setSortBy] = useState('created_at');

  // Toast state
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  const router = useRouter();

  useEffect(() => {
    const token = authService.getToken();
    if (!token) {
      router.push('/auth/login');
      return;
    }
    fetchTasks();

    // Connect to realtime service
    realtimeService.connect();

    // Subscribe to updates
    const unsubscribe = realtimeService.subscribe((data) => {
      console.log('Realtime update:', data);
      if (data.action === 'CREATED' || data.action === 'UPDATED' || data.action === 'DELETED' || data.action === 'COMPLETED') {
        fetchTasks();
        showToast(`Task update: ${data.action}`, 'success');
      }
    });

    return () => {
      unsubscribe();
      realtimeService.disconnect();
    };
  }, []);

  useEffect(() => {
    applyFiltersAndSort();
  }, [tasks, searchTerm, filterStatus, filterPriority, filterCategory, sortBy]);

  const showToast = (message: string, type: 'success' | 'error') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  const fetchTasks = async () => {
    try {
      const data = await taskService.getTasks();
      setTasks(data);
    } catch (err) {
      console.error('Failed to fetch tasks', err);
      showToast('Failed to fetch tasks', 'error');
    } finally {
      setLoading(false);
    }
  };

  const applyFiltersAndSort = () => {
    let filtered = [...tasks];

    if (searchTerm) {
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterStatus && filterStatus !== 'all') {
      filtered = filtered.filter(task => task.status === filterStatus);
    }

    if (filterPriority && filterPriority !== 'all') {
      filtered = filtered.filter(task => task.priority === filterPriority);
    }

    if (filterCategory) {
      filtered = filtered.filter(task =>
        task.category?.toLowerCase().includes(filterCategory.toLowerCase())
      );
    }

    filtered.sort((a, b) => {
      if (sortBy === 'created_at') {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      } else if (sortBy === 'title') {
        return a.title.localeCompare(b.title);
      } else if (sortBy === 'priority') {
        const priorityOrder = { high: 3, medium: 2, low: 1 };
        return priorityOrder[b.priority as keyof typeof priorityOrder] - priorityOrder[a.priority as keyof typeof priorityOrder];
      }
      return 0;
    });

    setFilteredTasks(filtered);
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTask.trim()) return;
    try {
      await taskService.createTask({
        title: newTask,
        priority: priority,
        category: category || undefined
      });
      setNewTask('');
      setCategory('');
      fetchTasks();
      showToast('Task created successfully!', 'success');
    } catch (err) {
      console.error('Failed to create task', err);
      showToast('Failed to create task', 'error');
    }
  };

  const toggleStatus = async (task: any) => {
    try {
      const newStatus = task.status === 'pending' ? 'completed' : 'pending';
      await taskService.updateTask(task.id, { status: newStatus });
      fetchTasks();
      showToast(`Task marked as ${newStatus}!`, 'success');
    } catch (err) {
      console.error('Failed to update status', err);
      showToast('Failed to update task', 'error');
    }
  };

  const deleteTask = async (id: string) => {
    try {
      await taskService.deleteTask(id);
      fetchTasks();
      showToast('Task deleted successfully!', 'success');
    } catch (err) {
      console.error('Failed to delete task', err);
      showToast('Failed to delete task', 'error');
    }
  };


  const clearFilters = () => {
    setSearchTerm('');
    setFilterStatus('all');
    setFilterPriority('all');
    setFilterCategory('');
    setSortBy('created_at');
  };

  const handleLogout = () => {
    authService.logout();
    router.push('/auth/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-4 md:p-8 transition-colors duration-300">
      <div className="max-w-7xl mx-auto">
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

        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">My Tasks</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm font-semibold text-white bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 rounded-lg shadow-md hover:shadow-lg transition-all duration-200"
          >
            Logout
          </button>
        </div>

        {/* Task Creation Form */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border-2 border-green-100 dark:border-green-900/30 mb-8 overflow-hidden transition-all duration-300">
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-gray-700 dark:to-gray-700/50 px-6 py-4 border-b-2 border-green-100 dark:border-green-900/30">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">Create New Task</h2>
            <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">Add a new task with priority and category</p>
          </div>
          <div className="p-6">
            <form onSubmit={handleCreateTask} className="space-y-4">
              <div className="flex flex-col sm:flex-row gap-3">
                <input
                  type="text"
                  value={newTask}
                  onChange={(e) => setNewTask(e.target.value)}
                  placeholder="Add a new task..."
                  className="flex-1 px-4 py-3 rounded-lg border-2 border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400 focus:border-green-500 dark:focus:border-green-400 focus:ring-4 focus:ring-green-100 dark:focus:ring-green-900/30 outline-none transition-all duration-200"
                />
                <button
                  type="submit"
                  className="px-8 py-3 text-sm font-semibold text-white bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
                >
                  Add Task
                </button>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">Priority</label>
                  <select
                    value={priority}
                    onChange={(e) => setPriority(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:border-green-500 dark:focus:border-green-400 focus:ring-4 focus:ring-green-100 dark:focus:ring-green-900/30 outline-none transition-all duration-200"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">Category</label>
                  <input
                    type="text"
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    placeholder="e.g. Work, Home"
                    className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400 focus:border-green-500 dark:focus:border-green-400 focus:ring-4 focus:ring-green-100 dark:focus:ring-green-900/30 outline-none transition-all duration-200"
                  />
                </div>
              </div>
            </form>
          </div>
        </div>

        {/* Search and Filter Panel */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border-2 border-gray-200 dark:border-gray-700 mb-8 overflow-hidden transition-all duration-300">
          <div className="px-6 py-4 border-b-2 border-gray-200 dark:border-gray-700 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">Search & Filter</h2>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">Find and organize your tasks</p>
            </div>
            <button
              onClick={clearFilters}
              className="px-4 py-2 text-sm font-semibold text-green-700 dark:text-green-300 bg-green-50 dark:bg-green-900/20 hover:bg-green-100 dark:hover:bg-green-900/40 border-2 border-green-200 dark:border-green-800 rounded-lg transition-all duration-200"
            >
              Clear All Filters
            </button>
          </div>
          <div className="p-6 space-y-4">
            {/* Search Bar */}
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search tasks..."
              className="w-full px-4 py-3 rounded-lg border-2 border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400 focus:border-green-500 dark:focus:border-green-400 focus:ring-4 focus:ring-green-100 dark:focus:ring-green-900/30 outline-none transition-all duration-200"
            />

            {/* Filters Row */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">Status</label>
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-lg border-2 border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:border-green-500 dark:focus:border-green-400 focus:ring-4 focus:ring-green-100 dark:focus:ring-green-900/30 outline-none transition-all duration-200"
                >
                  <option value="">All</option>
                  <option value="pending">Pending</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">Priority</label>
                <select
                  value={filterPriority}
                  onChange={(e) => setFilterPriority(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-lg border-2 border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:border-green-500 dark:focus:border-green-400 focus:ring-4 focus:ring-green-100 dark:focus:ring-green-900/30 outline-none transition-all duration-200"
                >
                  <option value="">All</option>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">Category</label>
                <input
                  type="text"
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  placeholder="Filter by category"
                  className="w-full px-4 py-2.5 rounded-lg border-2 border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-400 focus:border-green-500 dark:focus:border-green-400 focus:ring-4 focus:ring-green-100 dark:focus:ring-green-900/30 outline-none transition-all duration-200"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">Sort By</label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-lg border-2 border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:border-green-500 dark:focus:border-green-400 focus:ring-4 focus:ring-green-100 dark:focus:ring-green-900/30 outline-none transition-all duration-200"
                >
                  <option value="created_at">Date Created</option>
                  <option value="title">Title (A-Z)</option>
                  <option value="priority">Priority</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Tasks Count */}
        <div className="mb-4 text-sm font-semibold text-gray-600 dark:text-gray-400">
          Showing {filteredTasks.length} of {tasks.length} tasks
        </div>

        {/* Tasks List */}
        {loading ? (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border-2 border-gray-200 dark:border-gray-700 p-16 transition-all duration-300">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-200 dark:border-gray-600 border-t-green-600 dark:border-t-green-400"></div>
              <p className="mt-4 text-gray-600 dark:text-gray-300 font-medium">Loading tasks...</p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredTasks.length === 0 ? (
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border-2 border-gray-200 dark:border-gray-700 p-16 text-center transition-all duration-300">
                <div className="text-6xl mb-4">📋</div>
                <p className="text-gray-600 dark:text-gray-300 text-lg">
                  {tasks.length === 0 ? 'No tasks yet. Start by adding one above!' : 'No tasks match your filters.'}
                </p>
              </div>
            ) : (
              filteredTasks.map((task) => (
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
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}
