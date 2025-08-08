export default function Home() {
  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif', color: 'white', background: '#0a0a0a' }}>
      <h1>🚀 superNova_2177</h1>
      <p>Welcome to the interactive universe feed — symbolic only.</p>
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 3fr',
        gap: '1rem',
        marginTop: '2rem'
      }}>
        <aside style={{ background: '#111', padding: '1rem', borderRadius: '12px' }}>
          <h3>Sidebar</h3>
          <ul>
            <li>Feed</li>
            <li>Messages</li>
            <li>Proposals</li>
          </ul>
        </aside>
        <section style={{ background: '#181818', padding: '1rem', borderRadius: '12px' }}>
          <h2>Universe Connections</h2>
          <p>Here we will render the 3D forking worlds and voting logic.</p>
        </section>
      </div>
    </main>
  );
}
