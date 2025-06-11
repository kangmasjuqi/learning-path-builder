// frontend/src/app/dashboard/educator/page.tsx
"use client"; // This is a Client Component

import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';
import AuthGuard from '@/components/AuthGuard'; // Our authentication guard
import apiClient from '@/lib/api'; // Our API client
import Link from 'next/link';
import LoadingSpinner from '@/components/LoadingSpinner'; // For data fetching
import { CourseOut } from '@/types/api'; // We'll create this type definition shortly

export default function EducatorDashboardPage() {
  const { user } = useSelector((state: RootState) => state.auth);
  const [courses, setCourses] = useState<CourseOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch educator's courses when component mounts
  useEffect(() => {
    const fetchCourses = async () => {
      if (!user?.id) return; // Only fetch if user ID is available
      setLoading(true);
      setError(null);
      try {
        // Fetch courses created by the current educator
        // Assuming an endpoint like /courses?educator_id=X or /users/me/courses
        // For now, we'll fetch all courses and filter, or fetch directly if API supports (better)
        const response = await apiClient.get<CourseOut[]>(`/api/v1/courses`, {
            params: { educator_id: user.id } // Pass educator_id as a query parameter
        });
        setCourses(response.data.filter(course => course.educator_id === user.id)); // Filter client-side if API doesn't filter
      } catch (err: any) {
        console.error("Failed to fetch courses:", err.response?.data || err.message);
        setError("Failed to load courses. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, [user]); // Re-fetch if user object changes

  // Clever: Define a simple CourseCard component for reusability
  const CourseCard = ({ course }: { course: CourseOut }) => (
    <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
      <h3 className="text-xl font-bold mb-2 text-gray-800">{course.title}</h3>
      <p className="text-gray-600 text-sm mb-4 line-clamp-2">{course.description}</p>
      <div className="flex justify-between items-center text-sm text-gray-500">
        <span>Lessons: {course.lessons?.length || 0}</span> {/* Assuming lessons are nested or fetched */}
        {/* Future: Add link to edit course, view stats */}
      </div>
      <div className="mt-4 flex space-x-2">
        <Link href={`/courses/${course.id}/edit`} className="bg-blue-500 text-white px-3 py-1 rounded-md text-sm hover:bg-blue-600">
          Manage
        </Link>
        {/* Link to view lessons for this course */}
        <Link href={`/courses/${course.id}`} className="bg-gray-300 text-gray-800 px-3 py-1 rounded-md text-sm hover:bg-gray-400">
          View
        </Link>
      </div>
    </div>
  );

  return (
    <AuthGuard roles={['educator']}> {/* Protect this page for educators only */}
      <div className="container mx-auto p-6">
        <h1 className="text-4xl font-extrabold text-gray-900 mb-6">
          Welcome, {user?.username || 'Educator'}!
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
          {/* Quick Stats Section */}
          <div className="bg-gradient-to-r from-blue-500 to-blue-700 text-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-2">Total Courses</h2>
            <p className="text-5xl font-extrabold">{courses.length}</p>
            <p className="text-sm opacity-80 mt-2">Courses you have created</p>
          </div>
          <div className="bg-gradient-to-r from-green-500 to-green-700 text-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-2">Total Students</h2>
            <p className="text-5xl font-extrabold">--</p> {/* Placeholder */}
            <p className="text-sm opacity-80 mt-2">Enrolled in your courses</p>
          </div>
          <div className="bg-gradient-to-r from-purple-500 to-purple-700 text-white p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold mb-2">Total Lessons</h2>
            <p className="text-5xl font-extrabold">
                {courses.reduce((acc, course) => acc + (course.lessons?.length || 0), 0)}
            </p>
            <p className="text-sm opacity-80 mt-2">Across all your courses</p>
          </div>
        </div>

        <div className="flex justify-between items-center mb-6">
          <h2 className="text-3xl font-bold text-gray-900">Your Courses</h2>
          <Link href="/courses/create" className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg shadow-md transition duration-200">
            + Create New Course
          </Link>
        </div>

        {loading ? (
          <LoadingSpinner />
        ) : error ? (
          <p className="text-red-500 text-center text-lg">{error}</p>
        ) : courses.length === 0 ? (
          <div className="bg-white p-6 rounded-lg shadow-md text-center py-10">
            <p className="text-gray-600 text-lg mb-4">You haven't created any courses yet!</p>
            <Link href="/courses/create" className="text-indigo-600 hover:underline font-semibold">
              Start by creating your first course.
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {courses.map((course) => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
        )}
      </div>
    </AuthGuard>
  );
}