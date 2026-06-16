import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-[#0B1220] flex items-center justify-center p-4">
      <div className="text-center max-w-md">
        <div className="text-6xl mb-6">🕵️</div>
        <h1 className="text-3xl font-bold mb-3">Page Not Found</h1>
        <p className="text-[#94A3B8] mb-8">This page doesn't exist or has been locked until you complete the current level.</p>
        <Link href="/" className="btn-primary inline-block">Back to Home</Link>
      </div>
    </div>
  );
}
