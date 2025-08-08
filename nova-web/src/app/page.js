import PostCard from "@/components/PostCard";

export const metadata = { title: "superNova_2177" };

export default function Home() {
  return (
    <div style={{ display:"grid", gap:14 }}>
      <h2>Prototype feed (symbolic only)</h2>
      <PostCard />
      <PostCard title="Brian Wallace" subtitle="Aid worker at Garcia, Robinson and Joseph • 2nd" />
      <PostCard title="Rebecca Bauer" subtitle="Herbalist at Cooper, Clark and Wallace • 1st" />
    </div>
  );
}
