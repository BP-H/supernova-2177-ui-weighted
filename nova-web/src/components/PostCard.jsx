export default function PostCard({ post }) {
  return (
    <div style={{
      border:"1px solid rgba(122,162,255,.08)",
      borderRadius:16, padding:16, margin:"16px 0",
      background:"linear-gradient(180deg,rgba(255,255,255,.02),rgba(255,255,255,0))"
    }}>
      <div style={{display:"flex",gap:12,alignItems:"center"}}>
        <img src={post.author_avatar} alt="" width={40} height={40} style={{borderRadius:"50%"}} />
        <div>
          <div style={{fontWeight:700}}>{post.author_name}</div>
          <div style={{opacity:.7, fontSize:13}}>{post.author_title}</div>
        </div>
      </div>
      <p style={{marginTop:12}}>{post.text}</p>
      {post.image_url && (
        <img src={post.image_url} alt="" style={{width:"100%", borderRadius:12, marginTop:8}} />
      )}
      <div style={{opacity:.7, fontSize:13, marginTop:8}}>
        {post.stats.likes} likes • {post.stats.comments} comments • {post.stats.reposts} reposts
      </div>
    </div>
  );
}
