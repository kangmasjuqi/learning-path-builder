// frontend/src/app/login/page.tsx
"use client"; // <<< IMPORTANT: This page uses React hooks and client-side logic

import { useState, FormEvent } from 'react'; // React hooks for state and form event
import { useRouter } from 'next/navigation'; // Next.js hook for client-side navigation
import { useDispatch, useSelector } from 'react-redux'; // Redux hooks to interact with the store
import { AppDispatch, RootState } from '../../store'; // Type definitions for Redux store
import { loginStart, loginSuccess, loginFailure } from '../../store/slices/authSlice'; // Authentication actions
import apiClient from '../../lib/api'; // Our configured Axios API client
import Link from 'next/link'; // For linking to the registration page

export default function LoginPage() {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const dispatch: AppDispatch = useDispatch(); // Get the Redux dispatch function
  // Select relevant state from Redux store for loading, error, and authentication status
  const { loading, error, isAuthenticated } = useSelector((state: RootState) => state.auth);
  const router = useRouter(); // Initialize Next.js router

  // Clever: Redirect authenticated users away from the login page
  // This runs on every render to ensure the user is always on the correct page
  if (isAuthenticated) {
    // Use replace to prevent going back to login page with browser's back button
    router.replace('/dashboard/student'); // Default dashboard for now, will be dynamic later
    return null; // Don't render the login form if redirecting
  }

  // Handle form submission
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault(); // Prevent default browser form submission behavior
    dispatch(loginStart()); // Inform Redux that login process has started (sets loading: true)

    try {
      // Careful: FastAPI's OAuth2PasswordRequestForm expects form-encoded data, not JSON.
      // URLSearchParams correctly formats this for axios.
        const loginResponse = await apiClient.post(
            '/token',
            new URLSearchParams({
                username,
                password,
                grant_type: 'password',
            }),
            {
                headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                },
            }
        );

      const { access_token } = loginResponse.data;

      // Clever: After getting the token, immediately fetch full user details.
      // Our JWT only contains some user data, but `/users/me` gives the complete `UserOut` schema.
        const userResponse = await apiClient.get('/users/me', {
        headers: {
            Authorization: `Bearer ${access_token}`,
        },
        });
        
      const user = userResponse.data; // This is the UserOut schema from your backend

      // Dispatch success action with full user data and access token
      dispatch(loginSuccess({ user, accessToken: access_token }));

      // Navigate based on user role (educator or student)
      router.replace(user.is_educator ? '/dashboard/educator' : '/dashboard/student');
    } catch (err: any) {
      // Careful: Handle API errors gracefully
      const errorMessage = err.response?.data?.detail || "Login failed. Please check your credentials.";
      console.error("Login failed:", errorMessage, err);
      dispatch(loginFailure(errorMessage)); // Dispatch failure action with error message
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Login</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-gray-700 text-sm font-bold mb-2">
              Username:
            </label>
            <input
              type="text"
              id="username"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-gray-700 text-sm font-bold mb-2">
              Password:
            </label>
            <input
              type="password"
              id="password"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className="text-red-500 text-sm text-center">{error}</p>}

          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
            <button
              type="submit"
              className={`bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200 ease-in-out ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              disabled={loading}
            >
              {loading ? 'Logging In...' : 'Login'}
            </button>
            <Link href="/register" className="text-blue-600 hover:text-blue-800 font-bold text-sm text-center sm:text-right">
              Don't have an account? Register
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}