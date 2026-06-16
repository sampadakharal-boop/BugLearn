import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'BugLearn - AI-Powered Bug Bounty Learning Platform',
  description: 'The world\'s first AI-driven Bug Bounty Learning, Voice Certification, and Progression-Locked Cybersecurity Academy.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-[#0B1220] text-[#F8FAFC]">
        {children}
      </body>
    </html>
  );
}
