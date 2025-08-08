'use client';

import { useEffect, useCallback } from 'react';
import styles from './HomePage.module.css'; // Import the CSS module

// --- Data for the Feed ---
// Storing content in an array makes it easy to manage.
const feedData = [
  {
    title: 'Reality #2177: The Neon Dimension',
    content: 'In this reality, consciousness flows through digital streams. The boundaries between thought and code have dissolved. Every interaction creates ripples across parallel universes.',
  },
  {
    title: 'Quantum Entanglement Alert',
    content: 'Multiple timelines are converging at this exact moment. Observers report seeing their alternate selves in reflections. The fabric of spacetime feels unusually thin today.',
  },
  {
    title: 'Portal Discovery: Dimension X-99',
    content: 'A new gateway has been discovered leading to a universe where physics works backwards. Time flows in reverse, gravity pushes instead of pulls, and light creates shadows.',
  },
];

// --- Sub-Components ---
// Breaking the UI into smaller pieces makes the code much cleaner.

// Component for the animated background. It has no logic, so it's simple.
function AnimatedBackground() {
  return (
    <>
      <div className={styles.stars} />
      <div className={`${styles.floatingOrb} ${styles.orb1}`} />
      <div className={`${styles.floatingOrb} ${styles.orb2}`} />
    </>
  );
}

// Component for a single feed card. It takes data as props.
function FeedCard({ title, content }) {
  return (
    <div className={styles.feedCard}>
      <h3>{title}</h3>
      <p>{content}</p>
    </div>
  );
}

// --- Main Page Component ---
export default function HomePage() {
  // A more performant way to handle the particle effect on mouse move.
  const handleMouseMove = useCallback((e) => {
    // requestAnimationFrame ensures the browser isn't overwhelmed.
    window.requestAnimationFrame(() => {
      if (Math.random() > 0.9) { // Keep the random throttle
        createParticle(e.pageX, e.pageY);
      }
    });
  }, []);

  const createParticle = (x, y) => {
    const particle = document.createElement('div');
    // Using a separate stylesheet for the particle is even better, but this is fine.
    particle.style.position = 'fixed';
    particle.style.pointerEvents = 'none';
    particle.style.borderRadius = '50%';
    particle.style.zIndex = '1000';
    particle.style.left = `${x}px`;
    particle.style.top = `${y}px`;
    particle.style.width = `${Math.random() * 20 + 10}px`;
    particle.style.height = particle.style.width;
    particle.style.background = `radial-gradient(circle, rgba(138, 56, 236, 0.8) 0%, transparent 70%)`;
    particle.style.transition = 'transform 3s ease-out, opacity 3s ease-out';
    particle.style.opacity = '1';
    document.body.appendChild(particle);

    // Animate and remove the particle
    setTimeout(() => {
        particle.style.transform = `translateY(-200px) scale(0.5)`;
        particle.style.opacity = '0';
        setTimeout(() => particle.remove(), 3000);
    }, 10);
  };
  
  // Set up the event listener when the component mounts.
  useEffect(() => {
    // Add the body class for global styles
    document.body.className = styles.globalBody;
    
    document.addEventListener('mousemove', handleMouseMove);
    // Cleanup function to remove the listener when the component unmounts.
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.body.className = ''; // Clean up body class
    }
  }, [handleMouseMove]);

  return (
    <div className={styles.multiverseContainer}>
      <AnimatedBackground />
      <main className={styles.contentWrapper}>
        <h1 className={styles.pageTitle}>MULTIVERSE FEED</h1>
        <div className={styles.feedContainer}>
          {/* Map over the data array to create the feed cards automatically */}
          {feedData.map((item, index) => (
            <FeedCard key={index} title={item.title} content={item.content} />
          ))}
        </div>
      </main>
    </div>
  );
}
