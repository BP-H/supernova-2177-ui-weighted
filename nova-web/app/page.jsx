import Link from 'next/link';

export default function Home() {
  return (
    <main style={{ padding: 24, maxWidth: 1100, margin: '0 auto' }}>
      <h1>superNova_2177</h1>
      <Link href="/multiverse" style={{ 
        padding: '10px 14px',
        borderRadius: 12,
        border: '1px solid #8338ec',
        color: '#8338ec',
        textDecoration: 'none'
      }}>
        Enter Multiverse →
      </Link>
    </main>
  );
}
