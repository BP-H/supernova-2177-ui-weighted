import Link from 'next/link';

export default function Feed() {
  return (
    <main style={{ padding: 24, maxWidth: 1100, margin: '0 auto' }}>
      <div style={{ marginBottom: 24 }}>
        <Link
          href="/"
          style={{ padding: '10px 14px', borderRadius: 12, border: '1px solid #2e374d', textDecoration: 'none' }}
        >
          ← Back to Home
        </Link>
      </div>

      <h1 style={{ fontSize: 24, marginBottom: 16 }}>Feed</h1>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {['First post', 'Second post', 'Third post'].map((title, i) => (
          <div
            key={i}
            style={{
              padding: 20,
              border: '1px solid #2e374d',
              borderRadius: 12,
              backgroundColor: '#11131a'
            }}
          >
            <h3 style={{ marginBottom: 8 }}>{title}</h3>
            <p style={{ opacity: 0.8 }}>Placeholder content. Replace with real data later.</p>
          </div>
        ))}
      </div>
    </main>
  );
}
