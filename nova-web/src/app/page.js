export const metadata = { title: "superNova_2177" };

export default function Home() {
  return (
    <div>
      <h2>Feed</h2>
      <p>Welcome to superNova_2177. Use the sidebar to navigate.</p>

      {/* Demo posts so you see something change */}
      <div style={{marginTop:16, display:"grid", gap:12}}>
        {[1,2,3].map(i => (
          <article key={i} style={{
            border:"1px solid #2a2f3d",
            borderRadius:12,
            padding:16,
            background:"#11131d"
          }}>
            <strong>Post #{i}</strong>
            <p style={{opacity:.85, marginTop:8}}>
              Prototype content — symbolic only.
            </p>
            <div style={{display:"flex", gap:10, marginTop:8}}>
              <button>👍 Like</button>
              <button>💬 Comment</button>
              <button>🔁 Share</button>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
