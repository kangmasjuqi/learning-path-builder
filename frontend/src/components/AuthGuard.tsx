// frontend/src/components/AuthGuard.tsx
"use client"; // <<< IMPORTANT: This component uses React hooks and client-side logic

import { useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useRouter } from 'next/navigation';
import { RootState } from '@/store';
import LoadingSpinner from './LoadingSpinner'; // Our loading spinner component

interface AuthGuardProps {
  children: React.ReactNode;
  roles?: Array<'student' | 'educator'>; // Optional: specify required roles
}

export default function AuthGuard({ children, roles }: AuthGuardProps) {
  // Select relevant state from Redux: authentication status, user details, and loading state
  const { isAuthenticated, user, loading: authLoading } = useSelector((state: RootState) => state.auth);
  const router = useRouter(); // Initialize Next.js router

  useEffect(() => {
    // Careful: This effect runs after initial render. During server-side rendering or initial client-side hydration,
    // `authLoading` might be true as we're attempting to rehydrate state from localStorage.
    // We only perform redirects once the auth state is stable (`!authLoading`).
    if (!authLoading) {
      if (!isAuthenticated) {
        // Clever: If not authenticated, redirect to login. Use `replace` to avoid back button issues.
        router.replace('/login');
      } else if (roles && user) {
        // If roles are specified, check if the authenticated user has any of the required roles
        const hasRequiredRole = roles.some(role => {
          if (role === 'educator' && user.is_educator) return true;
          if (role === 'student' && !user.is_educator) return true; // Assuming non-educator is a student
          return false;
        });

        if (!hasRequiredRole) {
          // If authenticated but unauthorized for this role, redirect to unauthorized page
          router.replace('/unauthorized');
        }
      }
    }
  }, [isAuthenticated, user, roles, router, authLoading]); // Dependencies for useEffect

  // Clever: Show a loading spinner during initial authentication check or when redirecting
  // This prevents content flicker or showing unauthorized content momentarily
  if (authLoading || (!isAuthenticated && !authLoading) || (roles && user && !roles.some(role => (role === 'educator' && user.is_educator) || (role === 'student' && !user.is_educator)))) {
    return <LoadingSpinner />;
  }

  // If authenticated and authorized, render the children components
  return <>{children}</>;
}