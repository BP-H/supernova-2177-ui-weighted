import Sidebar from '../components/Sidebar';
import TopBar from '../components/TopBar';
import Feed from './feed/page'; // or wherever your feed logic lives

export default function HomePage() {
  return (
    <div className="flex bg-black min-h-screen text-white">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <TopBar />
        <main className="p-4">
          <Feed />
        </main>
      </div>
    </div>
  );
}
