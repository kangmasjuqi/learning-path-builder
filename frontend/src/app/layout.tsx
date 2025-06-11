// frontend/src/app/layout.tsx (MODIFIED)
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { ReduxProvider } from '@/components/ReduxProvider';
import Navbar from '@/components/Navbar'; // Import Navbar component
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Interactive Learning Path Builder',
  description: 'A full-stack EdTech platform.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} flex flex-col min-h-screen`}> {/* Added flex classes for full height layout */}
        <ReduxProvider>
          <Navbar /> {/* Render the Navbar at the top */}
          {/* Main content area, takes available space and provides padding/centering */}
          <main className="container mx-auto p-4 flex-grow"> 
            {children}
          </main>
          {/* Optional: Add a Footer component here later if desired */}
        </ReduxProvider>
      </body>
    </html>
  );
}