import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest) {
  const auth = req.headers.get('authorization');
  if (!auth?.startsWith('Bearer ')) return NextResponse.json({ detail: 'Not authenticated' }, { status: 401 });
  return NextResponse.json([]);
}
