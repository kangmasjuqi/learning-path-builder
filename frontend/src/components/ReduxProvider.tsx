// frontend/src/components/ReduxProvider.tsx
"use client"; // <<< IMPORTANT: This directive marks it as a Client Component

import React from 'react';
import { Provider } from 'react-redux';
import { store, AppDispatch } from '../store';
import { setAuthFromStorage, loginSuccess } from '../store/slices/authSlice';
import { useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';

// Interface to precisely match the JWT payload from your backend
interface UserJwtPayload {
    sub: string;
    exp: number;
    scopes: string[];
    id: number;
    email: string;
    is_educator: boolean;
    is_active: boolean;
}

export function ReduxProvider({ children }: { children: React.ReactNode }) {
  const dispatch: AppDispatch = store.dispatch; // Access dispatch directly from the store

  useEffect(() => {
    // This effect runs only once on the client-side after component mounts
    if (typeof window !== 'undefined') { // Ensure we are in a browser environment
      const accessToken = localStorage.getItem('accessToken');
      if (accessToken) {
        try {
          const decodedToken = jwtDecode<UserJwtPayload>(accessToken);

          // Check if the token has expired
          // `exp` is in seconds, `Date.now()` is in milliseconds, so multiply `exp` by 1000
          if (decodedToken.exp * 1000 < Date.now()) {
            console.log("Access token expired. Clearing authentication.");
            dispatch(setAuthFromStorage(null)); // Token expired, clear Redux state
            localStorage.removeItem('accessToken'); // Remove invalid token from storage
          } else {
            // Token is valid: Rehydrate Redux state with user data from the token
            const user = {
                id: decodedToken.id,
                username: decodedToken.sub,
                email: decodedToken.email,
                is_educator: decodedToken.is_educator,
                is_active: decodedToken.is_active,
            };
            // Dispatch loginSuccess to fully set up the state as if a fresh login happened
            dispatch(loginSuccess({ user, accessToken }));
          }
        } catch (error) {
          // Handle cases where the token is malformed or decoding fails
          console.error("Failed to decode token from localStorage or token invalid:", error);
          dispatch(setAuthFromStorage(null)); // Clear auth state on error
          localStorage.removeItem('accessToken'); // Remove bad token from storage
        }
      }
    }
  }, [dispatch]); // Dependency array: ensures effect runs on mount and if dispatch changes (rare)

  return <Provider store={store}>{children}</Provider>;
}