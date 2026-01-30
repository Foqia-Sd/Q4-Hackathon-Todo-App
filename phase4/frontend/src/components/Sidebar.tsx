'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import {
  LayoutDashboard,
  CheckSquare,
  Archive,
  User as UserIcon,
  Bot,
  LogOut,
  X
} from 'lucide-react';
import { authService } from '@/services/auth';

interface SidebarProps {
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
}

interface MenuItem {
  text: string;
  icon: React.ReactNode;
  path: string;
  action?: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isSidebarOpen, toggleSidebar }) => {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    authService.logout();
    router.push('/auth/login');
  };

  const menuItems: MenuItem[] = [
    { text: 'Dashboard', icon: <LayoutDashboard className="w-5 h-5" />, path: '/dashboard' },
    { text: 'My Tasks', icon: <CheckSquare className="w-5 h-5" />, path: '/dashboard/tasks' },
    { text: 'Completed', icon: <Archive className="w-5 h-5" />, path: '/dashboard/completed' },
    { text: 'Profile', icon: <UserIcon className="w-5 h-5" />, path: '/dashboard/profile' },
    { text: 'AI Chat', icon: <Bot className="w-5 h-5" />, path: '/dashboard/chat' },
  ];

  const logoutItem: MenuItem = {
    text: 'Logout',
    icon: <LogOut className="w-5 h-5" />,
    path: '#',
    action: handleLogout
  };

  return (
    <>
      {/* Overlay for mobile */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 z-50 h-full w-64 bg-gradient-to-b from-blue-600 to-blue-700 dark:from-gray-800 dark:to-gray-900 transform transition-transform duration-300 ease-in-out ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } md:translate-x-0 md:static md:z-auto shadow-xl`}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-blue-500/30 dark:border-gray-700">
          <h1 className="text-xl font-bold text-white">Todo App</h1>
          <button
            onClick={toggleSidebar}
            className="md:hidden text-white hover:bg-blue-500/30 dark:hover:bg-gray-700 rounded-lg p-1 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1">
          {menuItems.map((item) => {
            const isActive = pathname === item.path;

            return (
              <Link
                key={item.text}
                href={item.path}
                onClick={toggleSidebar}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg text-white transition-all duration-200 ${
                  isActive
                    ? 'bg-white/20 dark:bg-gray-700 shadow-md'
                    : 'hover:bg-white/10 dark:hover:bg-gray-700/50'
                }`}
              >
                <span className={isActive ? 'text-white' : 'text-blue-200 dark:text-gray-400'}>
                  {item.icon}
                </span>
                <span className="font-medium">{item.text}</span>
              </Link>
            );
          })}
        </nav>

        {/* Logout Button */}
        <div className="px-3 py-4 border-t border-blue-500/30 dark:border-gray-700">
          <button
            onClick={() => {
              toggleSidebar();
              logoutItem.action?.();
            }}
            className="flex items-center gap-3 w-full px-4 py-3 rounded-lg text-white hover:bg-red-500/20 dark:hover:bg-red-900/30 transition-all duration-200"
          >
            <span className="text-red-300 dark:text-red-400">
              {logoutItem.icon}
            </span>
            <span className="font-medium">{logoutItem.text}</span>
          </button>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
