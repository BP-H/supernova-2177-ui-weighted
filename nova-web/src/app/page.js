export default function Home() {
  return (
    <div style={{ display: 'flex', height: '100vh', background: '#0b0d17', color: 'white' }}>
      {/* Sidebar */}
      <div style={{ width: '250px', background: '#11131a', padding: '1rem' }}>
        <h2>superNova_2177</h2>
        <ul>
          <li>Feed</li>
          <li>Messages</li>
          <li>Decisions</li>
          <li>Profile</li>
        </ul>
      </div>

      {/* Main UI */}
      <div style={{ flex: 1, padding: '2rem' }}>
        <h1>🚀 The Cool UI Goes Here</h1>
        <p>This is where we can hook in your supernova_2177.py voting + 3D connections.</p>
      </div>
    </div>
  );
}
