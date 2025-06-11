// frontend/src/components/Navbar.tsx
"use client"; // <<< IMPORTANT: This component uses React hooks and client-side logic

import Link from 'next/link';
import { useDispatch, useSelector } from 'react-redux';
import { RootState, AppDispatch } from '../store'; // Redux types
import { logout } from '../store/slices/authSlice'; // Logout action
import { useRouter } from 'next/navigation'; // Next.js router for navigation

export default function Navbar() {
  const dispatch: AppDispatch = useDispatch();
  const router = useRouter();
  // Select authentication state and user details from Redux
  const { isAuthenticated, user } = useSelector((state: RootState) => state.auth);

  // Handle user logout
  const handleLogout = () => {
    dispatch(logout()); // Dispatch the logout action to clear Redux state and localStorage
    router.replace('/login'); // Redirect to login page after logout
  };

  return (
    <nav className="bg-blue-700 p-4 shadow-lg">
      <div className="container mx-auto flex flex-col sm:flex-row justify-between items-center">
        <Link href="/" className="text-white text-3xl font-extrabold mb-2 sm:mb-0 hover:text-blue-100 transition-colors duration-200">
          LearnPath
        </Link>
        <div className="flex flex-wrap justify-center sm:justify-end items-center space-x-4 text-lg">
          {isAuthenticated ? (
            <>
              <Link href="/courses" className="text-white hover:text-blue-200 transition-colors duration-200">
                Courses
              </Link>
              {user?.is_educator ? (
                <Link href="/dashboard/educator" className="text-white hover:text-blue-200 transition-colors duration-200">
                  Educator Dashboard
                </Link>
              ) : (
                <Link href="/dashboard/student" className="text-white hover:text-blue-200 transition-colors duration-200">
                  Student Dashboard
                </Link>
              )}
              <span className="text-blue-200 hidden md:inline">|</span> {/* Separator for larger screens */}
              <button
                onClick={handleLogout}
                className="text-white bg-blue-800 px-4 py-2 rounded-lg hover:bg-blue-900 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-300"
              >
                Logout ({user?.username})
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="text-white hover:text-blue-200 transition-colors duration-200">
                Login
              </Link>
              <Link href="/register" className="text-white hover:text-blue-200 transition-colors duration-200">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}