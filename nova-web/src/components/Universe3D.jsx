'use client';

import Link from 'next/link';
import { useEffect } from 'react';

export default function Multiverse() {
  useEffect(() => {
    // --- Interactive bits: particles + parallax + card glitch ---
    const onMove = (e) => {
      // CSS vars for pointer
      document.documentElement.style.setProperty('--px', `${e.clientX}px`);
      document.documentElement.style.setProperty('--py', `${e.clientY}px`);

      // Light parallax on orbs
      const cx = window.innerWidth / 2;
      const cy = window.innerHeight / 2;
      const dx = (e.clientX - cx) / cx; // -1..1
      const dy = (e.clientY - cy) / cy; // -1..1

      for (const [sel, mult] of [
        ['.orb1', 12],
        ['.orb2', -16],
        ['.orb3', 8],
      ]) {
        const el = document.querySelector(sel);
        if (el) el.style.transform = `translate(${dx * mult}px, ${dy * mult}px) scale(1)`;
      }

      // Occasionally spawn a particle
      if (Math.random() > 0.94) spawnParticle(e.pageX, e.pageY);
    };

    const spawnParticle = (x, y) => {
      const p = document.createElement('div');
      p.className = 'particle';
      p.style.left = `${x}px`;
      p.style.top = `${y}px`;

      const size = Math.random() * 12 + 6;
      p.style.width = `${size}px`;
      p.style.height = `${size}px`;
      p.style.borderRadius = '50%';

      const colors = ['#ff006e', '#8338ec', '#3a86ff', '#06ffa5', '#ffbe0b'];
      const c = colors[(Math.random() * colors.length) | 0];
      p.style.background = c;
      p.style.boxShadow = `0 0 ${size * 2}px ${c}`;

      document.body.appendChild(p);
      requestAnimationFrame(() => p.classList.add('active'));
      setTimeout(() => p.remove(), 2800);
    };

    const jitter = setInterval(() => {
      const cards = document.querySelectorAll('.feed-card');
      if (!cards.length) return;
      const c = cards[(Math.random() * cards.length) | 0];
      const x = (Math.random() * 4 - 2).toFixed(2);
      c.style.transform = `translateX(${x}px)`;
      setTimeout(() => (c.style.transform = ''), 100);
    }, 2400);

    window.addEventListener('mousemove', onMove);
    return () => {
      window.removeEventListener('mousemove', onMove);
      clearInterval(jitter);
    };
  }, []);

  return (
    <main className="mv-container">
      {/* Multiverse Background Layers */}
      <div className="multiverse-bg">
        <div className="stars stars-a" />
        <div className="stars stars-b" />
        <div className="grid-scan" />
        <div className="orb orb1" />
        <div className="orb orb2" />
        <div className="orb orb3" />
        <div className="portal" />
        <div className="cursor-glow" />
      </div>

      {/* Content */}
      <div className="content">
        <Link href="/" className="back-btn">← Back to Home</Link>
        <h1>MULTIVERSE FEED</h1>

        {[
          ['Reality #2177: The Neon Dimension', 'In this reality, consciousness flows through digital streams. The boundaries between thought and code have dissolved. Every interaction creates ripples across parallel universes.'],
          ['Quantum Entanglement Alert', 'Multiple timelines converging. Observers report seeing alternate selves. The fabric of spacetime feels unusually thin today.'],
          ['Portal Discovery: Dimension X-99', 'A gateway to a universe where physics works backwards. Time flows in reverse; gravity pushes instead of pulls.'],
          ['Cosmic Message Intercepted', '"The observer changes the observed. Reality is what you make it. Break free from the simulation."'],
          ['Multiverse Weather Report', 'Expect dimensional storms in sectors 7–12. Probability fluctuations may cause temporary reality glitches.'],
        ].map(([title, body], i) => (
          <article key={i} className="feed-card">
            <h3>{title}</h3>
            <p>{body}</p>
          </article>
        ))}
      </div>

      {/* Styles (scoped global for simplicity) */}
      <style jsx global>{`
        :root {
          --px: 50vw;
          --py: 50vh;
        }
        * { box-sizing: border-box; }
        body { background:#000; color:#fff; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        .mv-container { min-height:100vh; position:relative; overflow:hidden; }
        .multiverse-bg { position:fixed; inset:0; z-index:0; background: radial-gradient(ellipse at bottom, #101725 0%, #07080c 100%); }
        .stars { position:absolute; inset:0; background-repeat:repeat; background-size: 220px 220px; opacity:0.6; }
        .stars-a { 
          background-image:
            radial-gradient(2px 2px at 20px 30px, #eee, transparent),
            radial-gradient(1px 1px at 80px 10px, #eee, transparent),
            radial-gradient(2px 2px at 130px 80px, #eee, transparent);
          animation: drift 28s linear infinite;
        }
        .stars-b {
          background-image:
            radial-gradient(1px 1px at 40px 70px, #9fd, transparent),
            radial-gradient(1px 1px at 50px 50px, #cdf, transparent),
            radial-gradient(2px 2px at 110px 120px, #eef, transparent);
          animation: drift 38s linear infinite reverse;
          opacity:0.4;
        }
        @keyframes drift { 
          0% { transform: translate3d(0,0,0) scale(1); } 
          50% { transform: translate3d(-3%, -3%, 0) scale(1.05) rotate(0.5deg); } 
          100% { transform: translate3d(0,0,0) scale(1); } 
        }

        /* Scanline haze */
        .grid-scan {
          position:absolute; inset:0;
          background: repeating-linear-gradient( to bottom, rgba(255,255,255,0.03) 0px, rgba(255,255,255,0.03) 1px, transparent 2px, transparent 4px );
          mix-blend-mode: screen; opacity:0.25; pointer-events:none;
          animation: scan 4s linear infinite;
        }
        @keyframes scan { 0% { transform: translateY(-10%); } 100% { transform: translateY(10%); } }

        /* Parallax orbs */
        .orb { position:absolute; border-radius:50%; filter: blur(38px) saturate(120%); mix-blend-mode: screen; }
        .orb1 { width:400px; height:400px; background: radial-gradient(circle, rgba(138,43,226,0.35) 0%, transparent 70%); top:-160px; left:-180px; }
        .orb2 { width:320px; height:320px; background: radial-gradient(circle, rgba(0,191,255,0.35) 0%, transparent 70%); bottom:-160px; right:-160px; }
        .orb3 { width:520px; height:520px; background: radial-gradient(circle, rgba(255,0,128,0.28) 0%, transparent 70%); top:45%; left:50%; transform: translate(-50%,-50%); }

        /* Portal swirl */
        .portal {
          position:absolute; top:10%; right:10%; width:160px; height:160px; border-radius:50%;
          background: conic-gradient(from 0deg, #ff006e, #8338ec, #3a86ff, #06ffa5, #ffbe0b, #fb5607, #ff006e);
          animation: spin 3.5s linear infinite; filter: blur(22px); opacity:0.65; mix-blend-mode: screen;
        }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

        /* Pointer glow */
        .cursor-glow {
          position:absolute; width:36vmax; height:36vmax; border-radius:50%;
          left: calc(var(--px) - 18vmax); top: calc(var(--py) - 18vmax);
          background: radial-gradient(circle at center, rgba(131,56,236,0.25), rgba(0,0,0,0) 60%);
          pointer-events:none; transition: left 80ms linear, top 80ms linear;
          mix-blend-mode: screen; filter: blur(18px);
        }

        /* Content */
        .content { position:relative; z-index:1; max-width:1100px; margin:0 auto; padding:24px; }
        .back-btn {
          display:inline-block; padding:12px 20px; background: rgba(255,255,255,0.08);
          border:1px solid rgba(255,255,255,0.18); border-radius:50px; color:#fff; text-decoration:none;
          backdrop-filter: blur(10px); transition: all .25s ease;
        }
        .back-btn:hover { background: rgba(255,255,255,0.16); transform: translateX(-4px); box-shadow: 0 0 30px rgba(138,43,226,0.45); }

        h1 {
          font-size: clamp(2.4rem, 6vw, 4rem); font-weight: 800; margin: 28px 0 34px; letter-spacing: 0.02em;
          text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #8338ec, 0 0 40px #8338ec;
          animation: title-glitch 2.2s infinite;
        }
        @keyframes title-glitch {
          0%,100% { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #8338ec, 0 0 40px #8338ec; }
          25% { text-shadow: -2px 0 #ff006e, 2px 0 #06ffa5, 0 0 10px #fff, 0 0 20px #fff; }
          50% { text-shadow: 2px 0 #3a86ff, -2px 0 #ffbe0b, 0 0 10px #fff, 0 0 20px #fff; }
        }

        .feed-card {
          background: rgba(255,255,255,0.05);
          border: 1px solid rgba(255,255,255,0.12);
          border-radius: 20px;
          padding: 28px;
          margin-bottom: 26px;
          backdrop-filter: blur(18px);
          position: relative; overflow: hidden; transition: all .25s ease;
        }
        .feed-card::before {
          content:''; position:absolute; inset:0; left:-120%; background: linear-gradient(90deg, transparent, rgba(138,43,226,0.28), transparent);
          transition: left .5s ease;
        }
        .feed-card:hover::before { left: 120%; }
        .feed-card:hover { transform: translateY(-6px); border-color: rgba(138,43,226,0.45); box-shadow: 0 10px 40px rgba(138,43,226,0.26), 0 0 60px rgba(138,43,226,0.08); }
        .feed-card h3 {
          font-size: 1.5rem; margin-bottom: 10px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color: transparent;
        }
        .feed-card p { color: rgba(255,255,255,0.82); line-height: 1.6; }

        /* Particle animation */
        .particle { position: fixed; pointer-events: none; opacity: 0; z-index: 1; }
        .particle.active { animation: particle-float 2.8s ease-out forwards; }
        @keyframes particle-float {
          0% { opacity:0; transform: translateY(0) scale(0); }
          18% { opacity:1; transform: translateY(-14px) scale(1); }
          100% { opacity:0; transform: translateY(-180px) scale(0.5); }
        }
      `}</style>
    </main>
  );
}
