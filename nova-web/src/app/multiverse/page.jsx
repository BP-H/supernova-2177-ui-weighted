'use client'; // This makes it fun and interactive!

import Link from 'next/link';
import { useEffect } from 'react';

export default function Multiverse() {
  useEffect(() => {
    // Fun particles on mouse move (if you want this – skip if not needed)
    const handleMouseMove = (e) => {
      if (Math.random() > 0.95) {
        createParticle(e.pageX, e.pageY);
      }
    };

    const createParticle = (x, y) => {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = `${x}px`;
      particle.style.top = `${y}px`;
      particle.style.background = `radial-gradient(circle, rgba(138,56,236,0.8) 0%, transparent 70%)`;
      particle.style.width = `${Math.random() * 20 + 10}px`;
      particle.style.height = particle.style.width;
      document.body.appendChild(particle);
      particle.classList.add('active');
      setTimeout(() => particle.remove(), 3000);
    };

    document.addEventListener('mousemove', handleMouseMove);
    return () => document.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <>
      <style jsx global>{`
        body {
          margin: 0;
          background: black;
          color: white;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
          overflow-x: hidden;
        }

        .multiverse-container {
          position: relative;
          min-height: 100vh;
          overflow: hidden;
        }

        .stars {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-image: 
            radial-gradient(2px 2px at 20px 30px, white, transparent),
            radial-gradient(2px 2px at 40px 70px, white, transparent),
            radial-gradient(1px 1px at 50px 50px, white, transparent),
            radial-gradient(1px 1px at 80px 10px, white, transparent),
            radial-gradient(2px 2px at 130px 80px, white, transparent);
          background-repeat: repeat;
          background-size: 200px 200px;
          opacity: 0.3;
          animation: drift 20s linear infinite;
        }

        .stars::after {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-position: 100px 100px;
          animation-duration: 30s;
          animation-direction: reverse;
          opacity: 0.2;
        }

        @keyframes drift {
          from { transform: translate(0, 0); }
          to { transform: translate(-200px, -200px); }
        }

        .portal {
          position: absolute;
          top: 10%;
          right: 10%;
          width: 150px;
          height: 150px;
          border-radius: 50%;
          background: conic-gradient(from 0deg, #ff006e, #8338ec, #3a86ff, #06ffa5, #ffbe0b, #fb5607, #ff006e);
          animation: spin 3s linear infinite;
          filter: blur(20px);
          opacity: 0.7;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .content-wrapper {
          position: relative;
          z-index: 1;
          max-width: 1100px;
          margin: 0 auto;
          padding: 24px;
        }

        .back-link {
          display: inline-block;
          padding: 12px 20px;
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 50px;
          color: white;
          text-decoration: none;
          backdrop-filter: blur(10px);
          transition: all 0.3s ease;
        }

        .back-link:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateX(-5px);
          box-shadow: 0 0 30px rgba(138, 56, 236, 0.5);
        }

        h1 {
          font-size: 4rem;
          font-weight: 800;
          margin: 30px 0;
          text-align: center;
          text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #8338ec, 0 0 40px #8338ec;
          animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
          from { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #8338ec, 0 0 40px #8338ec; }
          to { text-shadow: 0 0 20px #fff, 0 0 30px #fff, 0 0 40px #8338ec, 0 0 50px #8338ec; }
        }

        .feed-container {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .feed-card {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 20px;
          padding: 30px;
          backdrop-filter: blur(10px);
          position: relative;
          overflow: hidden;
          transition: all 0.3s ease;
        }

        .feed-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: -100%;
          width: 100%;
          height: 100%;
          background: linear-gradient(90deg, transparent, rgba(138, 56, 236, 0.3), transparent);
          transition: left 0.5s ease;
        }

        .feed-card:hover::before {
          left: 100%;
        }

        .feed-card:hover {
          transform: translateY(-5px);
          border-color: rgba(138, 56, 236, 0.5);
          box-shadow: 0 10px 40px rgba(138, 56, 236, 0.3);
        }

        .feed-card h3 {
          font-size: 1.5rem;
          margin-bottom: 10px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip: text;
          background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .feed-card p {
          color: rgba(255, 255, 255, 0.8);
          line-height: 1.6;
        }

        .particle {
          position: fixed;
          pointer-events: none;
          border-radius: 50%;
          opacity: 0;
          z-index: 1000;
        }

        .particle.active {
          animation: float-up 3s ease-out forwards;
        }

        @keyframes float-up {
          0% { opacity: 0; transform: translateY(0) scale(0); }
          20% { opacity: 1; transform: translateY(-20px) scale(1); }
          100% { opacity: 0; transform: translateY(-200px) scale(0.5); }
        }

        .floating-orb {
          position: absolute;
          border-radius: 50%;
          filter: blur(40px);
          animation: float 10s ease-in-out infinite;
        }

        .orb1 {
          width: 300px;
          height: 300px;
          background: radial-gradient(circle, rgba(138, 56, 236, 0.4) 0%, transparent 70%);
          top: -100px;
          left: -100px;
          animation-duration: 15s;
        }

        .orb2 {
          width: 200px;
          height: 200px;
          background: radial-gradient(circle, rgba(0, 191, 255, 0.4) 0%, transparent 70%);
          bottom: -50px;
          right: -50px;
          animation-duration: 20s;
          animation-delay: 5s;
        }

        @keyframes float {
          0%, 100% { transform: translate(0, 0) scale(1); }
          25% { transform: translate(30px, -30px) scale(1.1); }
          50% { transform: translate(-20px, 20px) scale(0.9); }
          75% { transform: translate(20px, 30px) scale(1.05); }
        }
      `}</style>

      <div className="multiverse-container">
        <div className="stars"></div>
        <div className="portal"></div>
        <div className="floating-orb orb1"></div>
        <div className="floating-orb orb2"></div>

        <div className="content-wrapper">
          <Link href="/" className="back-link">
            ← Back to Reality
          </Link>

          <h1>MULTIVERSE FEED</h1>

          <div className="feed-container">
            <div className="feed-card">
              <h3>Reality #2177: The Neon Dimension</h3>
              <p>In this reality, consciousness flows through digital streams. The boundaries between thought and code have dissolved. Every interaction creates ripples across parallel universes.</p>
            </div>

            <div className="feed-card">
              <h3>Quantum Entanglement Alert</h3>
              <p>Multiple timelines are converging at this exact moment. Observers report seeing their alternate selves in reflections. The fabric of spacetime feels unusually thin today.</p>
            </div>

            <div className="feed-card">
              <h3>Portal Discovery: Dimension X-99</h3>
              <p>A new gateway has been discovered leading to a universe where physics works backwards. Time flows in reverse, gravity pushes instead of pulls, and light creates shadows.</p>
            </div>

            <div className="feed-card">
              <h3>Cosmic Message Intercepted</h3>
              <p>Strange signals from the void. The message repeats: "The observer changes the observed. Reality is what you make it. Break free from the simulation."</p>
            </div>

            <div className="feed-card">
              <h3>Multiverse Weather Report</h3>
              <p>Expect dimensional storms in sectors 7 through 12. Probability fluctuations may cause temporary reality glitches. Keep your quantum anchors secured.</p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
