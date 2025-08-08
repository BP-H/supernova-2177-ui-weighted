export default function PostCard({ title="Ann Guzman", subtitle="Public relations officer at Silva Group • 1st", body="Prototype content — symbolic only." }) {
  return (
    <article className="sn-post">
      <div style={{ fontWeight:700 }}>{title}</div>
      <div style={{ opacity:.7, fontSize:13, marginBottom:8 }}>{subtitle}</div>
      <p style={{ margin:"6px 0 0" }}>{body}</p>
      <div className="sn-actions">
        <button>🔥 Like</button>
        <button>💬 Comment</button>
        <button>🔗 Share</button>
        <button style={{ outline:"2px solid rgba(255,255,255,.15)" }}>🧪 React</button>
      </div>
    </article>
  );
}
