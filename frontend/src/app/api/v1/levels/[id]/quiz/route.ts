import { NextRequest, NextResponse } from 'next/server';

const QUIZZES: Record<number, any> = {
  1: { questions: [{q:'What does DNS do?',opts:['Sends emails','Translates domains to IPs','Encrypts data','Hosts websites'],ans:1},{q:'What is a packet?',opts:['A network cable','A piece of data sent over a network','A type of server','A security protocol'],ans:1},{q:'In the client-server model, what is a browser?',opts:['Server','Client','Router','ISP'],ans:1}]},
};

export async function GET(req: NextRequest, { params }: { params: { id: string } }) {
  const auth = req.headers.get('authorization');
  if (!auth?.startsWith('Bearer ')) return NextResponse.json({ detail: 'Not authenticated' }, { status: 401 });
  const levelNum = parseInt(params.id);
  const quiz = QUIZZES[levelNum];
  if (!quiz) return NextResponse.json({ detail: 'Level not found' }, { status: 404 });
  const safe = quiz.questions.map((q: any, i: number) => ({ q: q.q, opts: q.opts, id: i }));
  return NextResponse.json({ level_number: levelNum, questions: safe });
}

export async function POST(req: NextRequest, { params }: { params: { id: string } }) {
  const auth = req.headers.get('authorization');
  if (!auth?.startsWith('Bearer ')) return NextResponse.json({ detail: 'Not authenticated' }, { status: 401 });
  const levelNum = parseInt(params.id);
  const quiz = QUIZZES[levelNum];
  if (!quiz) return NextResponse.json({ detail: 'Level not found' }, { status: 404 });
  const body = await req.json();
  const answers = body.answers || [];
  let correct = 0;
  const results = quiz.questions.map((q: any, i: number) => {
    const isCorrect = answers[i] === q.ans;
    if (isCorrect) correct++;
    return { id: i, correct: isCorrect, correct_answer: q.ans };
  });
  const passed = correct >= quiz.questions.length * 0.7;
  return NextResponse.json({ score: correct, total: quiz.questions.length, passed, results });
}
