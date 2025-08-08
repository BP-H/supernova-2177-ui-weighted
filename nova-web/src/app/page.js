import "./globals.css";
import Header from "../components/Header";
import PostCard from "../components/PostCard";

const DEMO = [
  {
    id: 1,
    author_name: "Ann Guzman",
    author_title: "PR Officer • 1st",
    author_avatar: "https://api.dicebear.com/7.x/thumbs/svg?seed=ann",
    text: "Prototype content — symbolic only.",
    image_url: null,
    stats: { likes: 0, comments: 0, reposts: 0 },
  }
];

export default function Page() {
  return (
    <>
      <Header />
      <main style={{maxWidth:900, margin:"24px auto", padding:"0 16px"}}>
        {DEMO.map(p => <PostCard key={p.id} post={p} />)}
      </main>
    </>
  );
}
