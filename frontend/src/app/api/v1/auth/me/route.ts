import { NextRequest, NextResponse } from 'next/server';

const users = [
  { id: 1, name: 'Demo Hunter', email: 'demo@buglearn.com', password: 'demo123', current_level: 1, xp_points: 0, created_at: new Date().toISOString() },
];

export async function GET(req: NextRequest) {
  const auth = req.headers.get('authorization');
  if (!auth?.startsWith('Bearer ')) {
    return NextResponse.json({ detail: 'Not authenticated' }, { status: 401 });
  }
  try {
    const payload = JSON.parse(Buffer.from(auth.slice(7), 'base64').toString());
    const user = users.find(u => u.id === payload.sub);
    if (!user) return NextResponse.json({ detail: 'User not found' }, { status: 404 });
    return NextResponse.json({
      id: user.id, name: user.name, email: user.email,
      current_level: user.current_level, xp_points: user.xp_points, created_at: user.created_at,
    });
  } catch {
    return NextResponse.json({ detail: 'Invalid token' }, { status: 401 });
  }
}
