import PostCard from "../components/PostCard";
import { demoPosts } from "../lib/demo";

export default function Page() {
  return (
    <div className="max-w-3xl mx-auto">
      <div className="text-2xl font-bold mb-2">superNova_2177 <span className="badge">Prototype feed (symbolic only)</span></div>
      <div className="text-sm text-[var(--muted)] mb-4">All metrics here are symbolic reputation/engagement — not financial.</div>

      {demoPosts.map(p => <PostCard key={p.id} post={p} />)}
    </div>
  );
}
