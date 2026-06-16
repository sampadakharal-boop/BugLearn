import { NextRequest, NextResponse } from 'next/server';

const LEVELS: Record<number, any> = {
  1: { title: 'Internet Basics', subtitle: 'Level 1: How the Internet Works', description: 'Understand the global network that powers everything.', topics: [{name:'What is the Internet?',content:'The internet is a global network of computers connected by cables, satellites, and wireless signals.',emoji:'🌐'},{name:'IP Addresses & Domain Names',content:'Every device has an IP address. Domain names are mapped to IPs via DNS.',emoji:'📟'},{name:'Packets, Routing & ISPs',content:'Data travels in packets. Routers direct traffic.',emoji:'📦'},{name:'The Client-Server Model',content:'Clients request data. Servers store and serve it.',emoji:'💻'}],interview_prompt:'Explain how a packet travels from your browser to a server and back.',key_concepts:['internet','packet','ip address','dns','client','server'],quiz:[{q:'What does DNS do?',opts:['Sends emails','Translates domains to IPs','Encrypts data','Hosts websites'],ans:1},{q:'What is a packet?',opts:['A network cable','A piece of data sent over a network','A type of server','A security protocol'],ans:1},{q:'In the client-server model, what is a browser?',opts:['Server','Client','Router','ISP'],ans:1}],xp_reward:100},
  2: {title:'Web Fundamentals',subtitle:'Level 2: HTML, CSS, JavaScript',description:'Learn the building blocks of every website.',topics:[{name:'HTML',content:'HTML defines page structure.',emoji:'📄'},{name:'CSS',content:'CSS controls layout and colors.',emoji:'🎨'},{name:'JavaScript',content:'JS makes pages interactive.',emoji:'⚡'}],interview_prompt:'Explain the roles of HTML, CSS, and JavaScript.',key_concepts:['html','css','javascript'],quiz:[{q:'What does HTML define?',opts:['Page styling','Page structure','Page behavior','Server logic'],ans:1},{q:'Where does JavaScript run?',opts:['Only on servers','In the browser','In databases','On routers'],ans:1},{q:'What tool lets you inspect HTML?',opts:['Text editor','Browser DevTools','Command prompt','Email client'],ans:1}],xp_reward:100},
};

const TOTAL_LEVELS = Object.keys(LEVELS).length;

export async function GET(req: NextRequest) {
  const auth = req.headers.get('authorization');
  if (!auth?.startsWith('Bearer ')) return NextResponse.json({ detail: 'Not authenticated' }, { status: 401 });
  const results = Object.entries(LEVELS).map(([num, data]) => ({
    level_number: parseInt(num), title: data.title, status: 'in_progress',
    interview_score: null, last_attempt_date: null, xp_reward: data.xp_reward,
  }));
  return NextResponse.json(results);
}
