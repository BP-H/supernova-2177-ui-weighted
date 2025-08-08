import Link from 'next/link';

export default function Home() {
  return (
    <main style={{ padding: '24px', maxWidth: 1100, margin: '0 auto', minHeight: '100vh', background: '#000', color: '#fff' }}>
      <h1 style={{ fontSize: '28px', marginBottom: '16px' }}>superNova_2177</h1>
      <p style={{ opacity: 0.8, marginBottom: '24px' }}>
        Minimal layout test. If you see this on Vercel, we’re good.
      </p>
      <div style={{ marginTop: '24px', display: 'flex', gap: '12px' }}>
        <Link
          href="/multiverse"
          style={{ padding: '10px 14px', borderRadius: '12px', border: '1px solid #2e374d', textDecoration: 'none', color: '#fff' }}
        >
          Enter Multiverse →
        </Link>
        <Link
          href="/feed"
          style={{ padding: '10px 14px', borderRadius: '12px', border: '1px solid #2e374d', textDecoration: 'none', color: '#fff' }}
        >
          Go to Feed →
        </Link>
      </div>
    </main>
  );
}
