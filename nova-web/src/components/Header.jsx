export default function Header() {
  return (
    <header style={{
      position: "sticky", top: 0, zIndex: 10, backdropFilter: "blur(8px)",
      background: "rgba(11,11,14,.6)", borderBottom: "1px solid #1f2330",
      padding: "12px 16px"
    }}>
      <div style={{display:"flex",gap:12,alignItems:"center"}}>
        <div style={{fontWeight:800, fontSize:20}}>superNova_2177</div>
        <div style={{opacity:.7, fontSize:14}}>Prototype</div>
      </div>
    </header>
  );
}
