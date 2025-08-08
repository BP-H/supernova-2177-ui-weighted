import Image from 'next/image';
import Header from '@/components/Header';
import PostCard from '@/components/PostCard';

const posts = [
  {
    id: 1,
    author: 'Rebecca Bauer',
    title: 'Herbalist at Cooper, Clark and Wallace • 1st',
    avatar: 'https://api.dicebear.com/7.x/thumbs/svg?seed=RebeccaBauer',
    text: 'Look: tiny moments of order inside chaos. What are you refining?',
    image: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format',
    stats: { likes: 97, comments: 20, reposts: 28, edited: true },
  },
  {
    id: 2,
    author: 'Robert Owens',
    title: 'Surveyor at Jones LLC • 3rd',
    avatar: 'https://api.dicebear.com/7.x/thumbs/svg?seed=RobertOwens',
    text: 'South of here, ideas sharpen into tools. Bring yours.',
    image: 'https://images.unsplash.com/photo-1519183071298-a2962be96f83?q=80&w=1600&auto=format',
    stats: { likes: 407, comments: 47, reposts: 6, edited: false },
  },
  {
    id: 3,
    author: 'Sophia Sanders DVM',
    title: 'PR officer at Silva Group • 1st',
    avatar: 'https://api.dicebear.com/7.x/thumbs/svg?seed=SophiaSanders',
    text: 'Available might fast minute create her.',
    image: 'https://picsum.photos/seed/snv2177/1600/900',
    stats: { likes: 480, comments: 98, reposts: 29, edited: true },
  },
];

export default function Page() {
  return (
    <main className="mx-auto max-w-5xl px-4 py-10">
      <Header />
      <div className="mt-6 space-y-8">
        {posts.map(p => <PostCard key={p.id} post={p} />)}
      </div>
    </main>
  );
}
