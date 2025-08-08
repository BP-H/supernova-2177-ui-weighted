import Link from 'next/link';

export default function Home() {
  return (
    <main style={{ padding: '24px', maxWidth: 1100, margin: '0 auto' }}>
      <h1>Welcome to Supernova!</h1>
      <div style={{ marginTop: 24, display: 'flex', gap: 12 }}>
        <Link href="/feed"
          style={{ padding: '10px 14px', borderRadius: 12, border: '1px solid #2e374d' }}>
          Go to Feed →
        </Link>
      </div>
    </main>
  );
}
