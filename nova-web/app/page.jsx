'use client';
import Link from 'next/link';
import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion'; // Import Framer Motion

export default function Multiverse() {
  useEffect(() => {
    // Particle creation on mouse move (interactive)
    const handleMouseMove = (e) => {
      if (Math.random() > 0.8) createParticle(e.clientX, e.clientY);
    };
    const createParticle = (x, y) => {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = `${x}px`;
      particle.style.top = `${y}px`;
      particle.style.background = ['#ff006e', '#8338ec', '#3a86ff'][Math.floor(Math.random() * 3)];
      document.body.appendChild(particle);
      setTimeout(() => particle.remove(), 2000);
    };
    document.addEventListener('mousemove', handleMouseMove);
    return () => document.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Card animation variants for glitch/hover
  const cardVariants = {
    initial: { scale: 1, rotate: 0 },
    hover: { scale: 1.05, rotate: Math.random() * 4 - 2, transition: { duration: 0.3 } },
    tap: { scale: 0.95 }
  };

  return (
    <motion.div 
      className="multiverse-container"
      initial={{ opacity: 0 }} 
      animate={{ opacity: 1 }} 
      transition={{ duration: 1 }}
    >
      <style jsx global>{`
        /* Your existing styles here, plus: */
        .particle { position: fixed; width: 10px; height: 10px; border-radius: 50%; opacity: 0.8; animation: fadeOut 2s; }
        @keyframes fadeOut { to { opacity: 0; transform: translateY(-50px); } }
        .feed-card { cursor: pointer; } /* For interactions */
      `}</style>
      <div className="stars" /> {/* Your existing background */}
      <div className="portal" /> {/* Spinning portal */}
      <div className="content-wrapper">
        <Link href="/" className="back-link">← Back to Reality</Link>
        <motion.h1 
          variants={{ hover: { color: '#8338ec' } }} 
          whileHover="hover"
        >
          MULTIVERSE FEED
        </motion.h1>
        <div className="feed-container">
          <AnimatePresence>
            {[
              { title: 'Reality #2177: The Neon Dimension', desc: 'In this reality, consciousness flows through digital streams.' },
              { title: 'Quantum Entanglement Alert', desc: 'Multiple timelines are converging at this exact moment.' },
              { title: 'Portal Discovery: Dimension X-99', desc: 'A new gateway has been discovered leading to a universe where physics works backwards.' }
            ].map((item, i) => (
              <motion.div
                key={i}
                className="feed-card"
                variants={cardVariants}
                initial="initial"
                whileHover="hover"
                whileTap="tap"
              >
                <h3>{item.title}</h3>
                <p>{item.desc}</p>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    </motion.div>
  );
}
