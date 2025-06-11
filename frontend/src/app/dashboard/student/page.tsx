// frontend/src/app/dashboard/student/page.tsx
"use client"; // This is a Client Component

import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';
import AuthGuard from '@/components/AuthGuard'; // Our authentication guard
import apiClient from '@/lib/api'; // Our API client
import Link from 'next/link';
import LoadingSpinner from '@/components/LoadingSpinner';
import { UserProgressOut } from '@/types/api'; // We'll create this type definition shortly
import { CourseOut, LessonOut } from '@/types/api'; // For nested data

export default function StudentDashboardPage() {
  const { user } = useSelector((state: RootState) => state.auth);
  const [progress, setProgress] = useState<UserProgressOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch student's progress when component mounts
  useEffect(() => {
    const fetchProgress = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.get<UserProgressOut[]>('/api/v1/progress/me');
        setProgress(response.data);
      } catch (err: any) {
        console.error("Failed to fetch progress:", err.response?.data || err.message);
        setError("Failed to load learning progress. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();
  }, []); // No dependencies needed, fetches once on mount

  // Clever: Function to find the last accessed lesson for a 'Continue Learning' section
  const getLastAccessedLesson = (): { lesson: LessonOut; course: CourseOut } | null => {
      if (!progress.length) return null;

      // Sort progress by last_accessed_at descending
      const sortedProgress = [...progress].sort((a, b) => {
          const dateA = new Date(a.last_accessed_at).getTime();
          const dateB = new Date(b.last_accessed_at).getTime();
          return dateB - dateA;
      });

      // Find the most recently accessed lesson that is not yet completed
      // Or the last completed one if all are completed
      for (const p of sortedProgress) {
          if (p.lesson && p.lesson.course) { // Ensure nested data exists (populated by backend)
              if (!p.is_completed) {
                  return { lesson: p.lesson, course: p.lesson.course };
              }
          }
      }
      // If all are completed, return the very last one accessed
      const lastCompleted = sortedProgress[0];
      if (lastCompleted && lastCompleted.lesson && lastCompleted.lesson.course) {
          return { lesson: lastCompleted.lesson, course: lastCompleted.lesson.course };
      }
      return null;
  };

  const lastAccessed = getLastAccessedLesson();

  return (
    <AuthGuard roles={['student']}> {/* Protect this page for students only */}
      <div className="container mx-auto p-6">
        <h1 className="text-4xl font-extrabold text-gray-900 mb-6">
          Welcome, {user?.username || 'Student'}!
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          {/* Continue Learning Section */}
          <div className="bg-white p-6 rounded-lg shadow-md border-t-4 border-blue-500">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">Continue Learning</h2>
            {loading ? (
              <LoadingSpinner />
            ) : lastAccessed ? (
              <div>
                <h3 className="text-xl font-semibold text-gray-700">{lastAccessed.lesson.title}</h3>
                <p className="text-gray-600 text-sm mb-2">{lastAccessed.course.title}</p>
                <Link
                  href={`/courses/<span class="math-inline">\{lastAccessed\.course\.id\}/lessons/</span>{lastAccessed.lesson.id}`}
                  className="bg-blue-500 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-600 transition-colors duration-200 mt-4 inline-block"
                >
                  Resume Lesson
                </Link>
              </div>
            ) : (
              <p className="text-gray-600">Start a new course to see your progress here!</p>
            )}
          </div>

          {/* My Learning Progress Stats (Placeholder) */}
          <div className="bg-white p-6 rounded-lg shadow-md border-t-4 border-green-500">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">My Progress</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-4xl font-bold text-green-600">{progress.filter(p => p.is_completed).length}</p>
                <p className="text-sm text-gray-500">Lessons Completed</p>
              </div>
              <div>
                <p className="text-4xl font-bold text-gray-700">{progress.length}</p>
                <p className="text-sm text-gray-500">Lessons Attempted</p>
              </div>
            </div>
            <Link href="/courses" className="text-blue-600 hover:underline text-sm mt-4 inline-block">
              Browse all courses &rarr;
            </Link>
          </div>
        </div>

        <h2 className="text-3xl font-bold text-gray-900 mb-6">Enrolled Courses (Coming Soon)</h2>
        <div className="bg-white p-6 rounded-lg shadow-md text-center py-10">
          <p className="text-gray-600 text-lg mb-4">
            You'll see your enrolled courses and detailed progress here.
          </p>
          <Link href="/courses" className="text-indigo-600 hover:underline font-semibold">
            Explore available courses.
          </Link>
        </div>
      </div>
    </AuthGuard>
  );
}