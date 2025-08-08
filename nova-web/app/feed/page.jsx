"use client";

export default function FeedPage() {
  return (
    <div style={{color:"#e9ecf1", fontFamily:"system-ui, sans-serif", padding:24}}>
      <h1 style={{fontWeight:800, marginBottom:8}}>superNova_2177</h1>
      <div style={{opacity:.7, marginBottom:16}}>Prototype feed (symbolic only)</div>

      <div style={{
        border:"1px solid #1c2130",
        background:"#11131d",
        borderRadius:16,
        padding:16,
        maxWidth:720
      }}>
        <div style={{fontWeight:600}}>Ann Guzman</div>
        <div style={{opacity:.7, fontSize:14, marginBottom:8}}>
          Public relations officer at Silva Group • 1st
        </div>
        <p>Prototype content — symbolic only.</p>
        <div style={{marginTop:12, display:"grid", gap:8, gridTemplateColumns:"repeat(4, minmax(0,1fr))"}}>
          <button>👍 Like</button>
          <button>💬 Comment</button>
          <button>📤 Share</button>
          <button>🔥 React</button>
        </div>
      </div>
    </div>
  );
}
