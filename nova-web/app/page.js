'use client';

import { Suspense, useEffect, useState, useRef, useMemo } from 'react';
import Link from 'next/link';
import { Canvas, useFrame } from '@react-three/fiber';
import { Points, PointMaterial } from '@react-three/drei';
import * as random from 'maath/random/dist/maath-random.esm';
import { 
  Home, 
  User, 
  MessageSquare, 
  Settings, 
  LayoutGrid,
  Vote,
  Bot
} from 'lucide-react';
import styles from './HomePage.module.css';

// --- 3D Background Component ---
function Stars3D(props) {
  const ref = useRef();
  const [sphere] = useState(() => random.inSphere(new Float32Array(5000), { radius: 1.2 }));

  useFrame((state, delta) => {
    ref.current.rotation.x -= delta / 10;
    ref.current.rotation.y -= delta / 15;
  });

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      <Points ref={ref} positions={sphere} stride={3} frustumCulled={false} {...props}>
        <PointMaterial
          transparent
          color="#9b8cff"
          size={0.005}
          sizeAttenuation={true}
          depthWrite={false}
        />
      </Points>
    </group>
  );
}

// --- UI Sub-Components ---
const NavLink = ({ href, icon: Icon, children }) => (
  <Link href={href} className={styles.navLink}>
    <Icon size={20} />
    <span>{children}</span>
  </Link>
);

function Sidebar() {
  const navItems = useMemo(() => [
    { href: '/', icon: Home, label: 'Feed' },
    { href: '/profile', icon: User, label: 'Profile' },
    { href: '/messages', icon: MessageSquare, label: 'Messages' },
    { href: '/proposals', icon: Vote, label: 'Proposals' },
    { href: '/agents', icon: Bot, label: 'Agents' },
    { href: '/settings', icon: Settings, label: 'Settings' },
  ], []);

  return (
    <aside className={styles.sidebar}>
      <div className={styles.sidebarHeader}>
        <LayoutGrid size={28} color="#9b8cff" />
        <span>superNova_2177</span>
      </div>
      <nav className={styles.sidebarNav}>
        {navItems.map(item => <NavLink key={item.label} {...item} />)}
      </nav>
    </aside>
  );
}

function FeedCard({ title, content, href }) {
  return (
    <Link href={href} className={styles.feedCardLink}>
      <div className={styles.feedCard}>
        <h3>{title}</h3>
        <p>{content}</p>
      </div>
    </Link>
  );
}

// --- Main Page Component ---
export default function HomePage() {
  const [feedData, setFeedData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    document.body.className = styles.globalBody;

    fetch('/api/feed')
      .then((res) => res.json())
      .then((apiResponse) => {
        setFeedData(apiResponse.data);
        setIsLoading(false);
      })
      .catch(error => {
        console.error("Failed to fetch feed data:", error);
        setIsLoading(false);
      });

    return () => {
      document.body.className = '';
    };
  }, []);

  return (
    <div className={styles.pageLayout}>
      <Sidebar />
      <main className={styles.mainContent}>
        <div className={styles.threeCanvas}>
          <Canvas camera={{ position: [0, 0, 1] }}>
            <Suspense fallback={null}>
              <Stars3D />
            </Suspense>
          </Canvas>
        </div>
        <div className={styles.contentWrapper}>
          <h1 className={styles.pageTitle}>
            <a
              href="https://superNova2177.com"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'inherit', textDecoration: 'none' }}
            >
              superNova2177.com
            </a>
          </h1>
          {isLoading ? (
            <p style={{ textAlign: 'center' }}>Loading feed from the cosmos...</p>
          ) : (
            <div className={styles.feedContainer}>
              {feedData.map((item) => (
                <FeedCard
                  key={item.id}
                  title={item.title}
                  content={item.content}
                  href={`/reality/${item.id}`}
                />
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
