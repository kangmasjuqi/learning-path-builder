// frontend/src/app/register/page.tsx
"use client"; // <<< IMPORTANT: This page uses React hooks and client-side logic

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import apiClient from '../../lib/api'; // Our configured Axios API client
import Link from 'next/link'; // For linking to the login page

export default function RegisterPage() {
  const [username, setUsername] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [isEducator, setIsEducator] = useState<boolean>(false); // Checkbox for educator role
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true); // Indicate loading state
    setError(null);    // Clear previous errors
    setSuccess(null);  // Clear previous success messages

    try {
      // Send registration data as JSON
      const response = await apiClient.post('/users/', {
        username,
        email,
        password,
        is_educator: isEducator, // Include the educator status
      });
      setSuccess("Registration successful! You can now log in.");
      // Clever: Automatically redirect to login after a short delay for user to read message
      setTimeout(() => {
        router.replace('/login');
      }, 2000);
    } catch (err: any) {
      // Careful: Extract meaningful error messages from API response
      const errorMessage = err.response?.data?.detail || "Registration failed. Please try again.";
      console.error("Registration failed:", errorMessage, err);
      setError(errorMessage);
    } finally {
      setLoading(false); // End loading state
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Register Account</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-gray-700 text-sm font-bold mb-2">
              Username:
            </label>
            <input
              type="text"
              id="username"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="email" className="block text-gray-700 text-sm font-bold mb-2">
              Email:
            </label>
            <input
              type="email"
              id="email"
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="flex items-center">
            <input
              type="checkbox"
              id="isEducator"
              className="form-checkbox h-4 w-4 text-green-600 transition duration-150 ease-in-out"
              checked={isEducator}
              onChange={(e) => setIsEducator(e.target.checked)}
            />
            <label htmlFor="isEducator" className="ml-2 block text-gray-700 text-sm font-bold">
              Register as an Educator?
            </label>
          </div>

          {error && <p className="text-red-500 text-sm text-center">{error}</p>}
          {success && <p className="text-green-500 text-sm text-center">{success}</p>}

          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
            <button
              type="submit"
              className={`bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200 ease-in-out ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              disabled={loading}
            >
              {loading ? 'Registering...' : 'Register'}
            </button>
            <Link href="/login" className="text-blue-600 hover:text-blue-800 font-bold text-sm text-center sm:text-right">
              Already have an account? Login
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}