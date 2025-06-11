// frontend/src/app/unauthorized/page.tsx
import Link from 'next/link';

export default function UnauthorizedPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md text-center">
        <h1 className="text-3xl font-bold text-red-600 mb-4">Access Denied</h1>
        <p className="text-gray-700 mb-6">You do not have the necessary permissions to view this page.</p>
        <Link href="/" className="text-blue-600 hover:underline font-bold">
          Go to Home
        </Link>
      </div>
    </div>
  );
}