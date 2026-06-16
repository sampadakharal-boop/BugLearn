import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  return NextResponse.json({ detail: 'Registration is disabled in demo. Use demo@buglearn.com / demo123' }, { status: 400 });
}
