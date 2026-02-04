import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center p-4 transition-colors duration-300">
      <div className="max-w-5xl mx-auto text-center">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border-2 border-green-100 dark:border-green-900/30 overflow-hidden transition-all duration-300">
          {/* Header Section */}
          <div className="space-y-6 p-8 md:p-16 bg-gradient-to-br from-white via-green-50/30 to-emerald-50/50 dark:from-gray-800 dark:via-gray-800 dark:to-gray-700/50">
            <h1 className="text-5xl md:text-7xl font-extrabold text-gray-900 dark:text-white mb-6 tracking-tight">
              Welcome to <span className="text-green-600 dark:text-green-400 inline-block hover:scale-105 transition-transform duration-200">Todo App</span>
            </h1>
            <p className="text-lg md:text-2xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto leading-relaxed">
              Organize your tasks efficiently with priorities, categories, and powerful search features.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
              <Link
                href="/auth/signup"
                className="inline-flex items-center justify-center px-8 py-4 text-base font-semibold text-white bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
              >
                Get Started
              </Link>
              <Link
                href="/auth/login"
                className="inline-flex items-center justify-center px-8 py-4 text-base font-semibold text-green-700 dark:text-green-300 bg-white dark:bg-gray-700 border-2 border-green-600 dark:border-green-500 hover:bg-green-50 dark:hover:bg-gray-600 rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
              >
                Login
              </Link>
            </div>
          </div>

          {/* Features Section */}
          <div className="p-8 md:p-16 pt-12">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
              {/* Feature 1 */}
              <div className="group bg-gradient-to-br from-green-50 to-emerald-50 dark:from-gray-700 dark:to-gray-700/50 border-2 border-green-200 dark:border-green-800/50 rounded-xl p-6 hover:shadow-xl hover:border-green-300 dark:hover:border-green-700 transition-all duration-300 hover:-translate-y-1">
                <div className="text-4xl mb-4 transform group-hover:scale-110 transition-transform duration-200">📝</div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Task Management</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Create, update, and organize your tasks with ease.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="group bg-gradient-to-br from-green-50 to-emerald-50 dark:from-gray-700 dark:to-gray-700/50 border-2 border-green-200 dark:border-green-800/50 rounded-xl p-6 hover:shadow-xl hover:border-green-300 dark:hover:border-green-700 transition-all duration-300 hover:-translate-y-1">
                <div className="text-4xl mb-4 transform group-hover:scale-110 transition-transform duration-200">🎯</div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Priorities & Categories</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Set priorities and categorize tasks for better organization.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="group bg-gradient-to-br from-green-50 to-emerald-50 dark:from-gray-700 dark:to-gray-700/50 border-2 border-green-200 dark:border-green-800/50 rounded-xl p-6 hover:shadow-xl hover:border-green-300 dark:hover:border-green-700 transition-all duration-300 hover:-translate-y-1">
                <div className="text-4xl mb-4 transform group-hover:scale-110 transition-transform duration-200">🔍</div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">Search & Filter</h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  Quickly find tasks with powerful search and filtering options.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
