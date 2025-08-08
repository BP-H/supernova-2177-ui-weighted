import Link from 'next/link';

export default function Home() {
  return (
    <main style={{ padding: 24, maxWidth: 1100, margin: '0 auto' }}>
      <h1 style={{ fontSize: 28, marginBottom: 16 }}>superNova_2177</h1>
      <p style={{ opacity: 0.8, marginBottom: 24 }}>
        Minimal layout test. If you see this on Vercel, we’re good.
      </p>

      <div style={{ marginTop: 24, display: 'flex', gap: 12 }}>
        <Link
          href="/feed"
          style={{ padding: '10px 14px', borderRadius: 12, border: '1px solid #2e374d', textDecoration: 'none' }}
        >
          Go to Feed →
        </Link>
      </div>
    </main>
  );
}
