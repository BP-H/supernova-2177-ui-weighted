import Link from 'next/link';

export default function Home() {
  return (
    <main style={{ padding: 24 }}>
      <h1>superNova_2177</h1>
      <Link href="/multiverse" style={{ color: '#8338ec' }}>
        Enter Multiverse →
      </Link>
    </main>
  );
}
