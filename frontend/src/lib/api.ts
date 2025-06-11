// frontend/src/lib/api.ts
import axios from 'axios';
import { store } from '../store'; // Import your Redux store
import { logout } from '../store/slices/authSlice'; // Import the logout action

// Retrieve the API base URL from the frontend's environment variables
// This variable is set in frontend/.env.local (e.g., http://localhost:8000/api/v1)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

// Create a custom Axios instance with a base URL and default headers
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: This runs before every request is sent.
apiClient.interceptors.request.use(
  (config) => {
    // Get the current authentication state from the Redux store
    const state = store.getState();
    const token = state.auth.accessToken; // Retrieve the access token

    // If a token exists, add it to the Authorization header in the 'Bearer' format
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config; // Return the modified request configuration
  },
  (error) => {
    // Handle any errors that occur during the request setup (e.g., network issues)
    return Promise.reject(error);
  }
);

// Response Interceptor: This runs after a response is received from the API.
apiClient.interceptors.response.use(
  (response) => response, // If the response is successful (2xx status), just pass it through
  async (error) => {
    // Check if the response error indicates an Unauthorized (401) status
    // and ensure it's not from the /token endpoint itself (which is for login, and expects 401 on failure)
    if (error.response?.status === 401 && error.config.url !== '/token') {
      console.warn("Unauthorized API request or token expired. Dispatching logout.");
      // Dispatch the logout action to clear the Redux state and localStorage
      store.dispatch(logout());

      // **Careful Note on Redirection:**
      // Directly using Next.js `router.push()` here in an Axios interceptor (which is a global, non-React component context)
      // can be tricky. For robustness, it's generally better for your React components
      // to observe the `isAuthenticated` state from Redux and perform redirects when it becomes `false`.
      // For now, if a user is on a protected page and their token expires (resulting in a 401),
      // the `AuthGuard` component (which we'll implement next) will detect the `isAuthenticated: false`
      // state change and handle the redirection to the login page.
    }
    return Promise.reject(error); // Re-throw the error so that the component making the request can catch it
  }
);

export default apiClient;