import PostCard from "../components/PostCard";
import { listFeed, healthz } from "../lib/api";

export default async function Page() {
  const [posts, hz] = await Promise.all([listFeed(), healthz()]);
  return (
    <div>
      {hz?.status !== "ok" && (
        <div className="mb-3 text-sm text-white/60">
          Backend offline — showing demo data.
        </div>
      )}
      {posts.map(p => <PostCard key={p.id} post={p} />)}
    </div>
  );
}
