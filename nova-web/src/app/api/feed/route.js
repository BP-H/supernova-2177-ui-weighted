// File: nova-web/src/app/api/feed/route.js
import { NextResponse } from 'next/server';

const feedData = [
  {
    id: 'reality-2177',
    title: 'Reality #2177: The Neon Dimension',
    content: 'In this reality, consciousness flows through digital streams. The boundaries between thought and code have dissolved.',
  },
  {
    id: 'quantum-alert',
    title: 'Quantum Entanglement Alert',
    content: 'Multiple timelines are converging at this exact moment. Observers report seeing their alternate selves in reflections.',
  },
  {
    id: 'portal-x99',
    title: 'Portal Discovery: Dimension X-99',
    content: 'A new gateway has been discovered leading to a universe where physics works backwards. Time flows in reverse.',
  },
];

export async function GET(request) {
  // In the future, you can replace this with a real call to your Python API
  return NextResponse.json({ data: feedData });
}
