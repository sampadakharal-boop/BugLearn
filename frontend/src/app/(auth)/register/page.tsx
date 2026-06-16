'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import Link from 'next/link';
import toast from 'react-hot-toast';

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await api.register(form.name, form.email, form.password);
      toast.success('Account created! Your journey begins.');
      router.push('/dashboard');
    } catch (err: any) {
      const msg = err.message || 'Registration failed';
      setError(msg);
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-grid flex items-center justify-center p-4">
      <div className="absolute top-6 left-6">
        <Link href="/" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#f59e0b] to-[#ef4444] flex items-center justify-center text-white font-bold text-sm">B</div>
          <span className="text-[#F8FAFC] font-bold">Bug<span className="text-[#f59e0b]">Learn</span></span>
        </Link>
      </div>

      <div className="glass-card w-full max-w-md p-8 glow">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#f59e0b] to-[#ef4444] flex items-center justify-center text-2xl mx-auto mb-4">⬡</div>
          <h1 className="text-2xl font-bold text-[#F8FAFC]">Start Your Journey</h1>
          <p className="text-[#94A3B8] text-sm mt-1">Begin your bug bounty learning path</p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs text-[#94A3B8] mb-1 font-mono">Full Name</label>
            <input type="text" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} className="input-field w-full" placeholder="Jane Doe" required />
          </div>
          <div>
            <label className="block text-xs text-[#94A3B8] mb-1 font-mono">Email</label>
            <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} className="input-field w-full" placeholder="hunter@example.com" required />
          </div>
          <div>
            <label className="block text-xs text-[#94A3B8] mb-1 font-mono">Password</label>
            <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} className="input-field w-full" placeholder="Min 8 characters" required minLength={8} />
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? 'Creating account...' : 'Begin Learning'}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-[#64748b]">
          Already have an account?{' '}
          <Link href="/login" className="text-[#f59e0b] hover:underline">Sign in</Link>
        </div>
      </div>
    </div>
  );
}
