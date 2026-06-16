import { NextRequest, NextResponse } from 'next/server';

const users = [
  { id: 1, name: 'Demo Hunter', email: 'demo@buglearn.com', password: 'demo123', current_level: 1, xp_points: 0, created_at: new Date().toISOString() },
];

export async function POST(req: NextRequest) {
  const { email, password } = await req.json();
  const user = users.find(u => u.email === email);
  if (!user || user.password !== password) {
    return NextResponse.json({ detail: 'Invalid email or password' }, { status: 401 });
  }
  const token = Buffer.from(JSON.stringify({ sub: user.id, email: user.email })).toString('base64');
  return NextResponse.json({
    access_token: token, token_type: 'bearer',
    user: { id: user.id, name: user.name, email: user.email, current_level: user.current_level, xp_points: user.xp_points, created_at: user.created_at },
  });
}
