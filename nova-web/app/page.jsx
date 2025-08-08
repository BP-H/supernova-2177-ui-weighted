import Link from 'next/link';

export default function Home() {
  return (
    <main style={{ padding: '24px', maxWidth: 1100, margin: '0 auto', background: 'black', color: 'white' }}>
      <h1 style={{ fontSize: '2rem', marginBottom: '16px' }}>SuperNova_2177</h1>
      <p style={{ marginBottom: '24px' }}>Welcome to the gateway of universes!</p>
      <div style={{ display: 'flex', gap: '12px' }}>
        <Link 
          href="/feed" 
          style={{ padding: '10px 14px', borderRadius: '12px', border: '1px solid #2e374d', color: 'white', textDecoration: 'none' }}>
          Go to Feed →
        </Link>
        <Link 
          href="/multiverse" 
          style={{ padding: '10px 14px', borderRadius: '12px', border: '1px solid #8338ec', color: '#8338ec', textDecoration: 'none' }}>
          Enter Multiverse →
        </Link>
      </div>
    </main>
  );
}
