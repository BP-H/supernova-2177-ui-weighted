"use client";

export default function FeedPage() {
  return (
    <div style={{color:"#e9ecf1"}}>
      <h2 style={{fontWeight:700, marginBottom:8}}>superNova_2177</h2>
      <div style={{opacity:.7, marginBottom:16}}>Prototype feed (symbolic only)</div>

      <div style={{border:"1px solid #1c2130", borderRadius:16, padding:16}}>
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
