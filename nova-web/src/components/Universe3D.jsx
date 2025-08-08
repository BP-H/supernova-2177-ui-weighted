'use client';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import { useRef } from 'react';

function Spinner(props) {
  const ref = useRef();
  return (
    <mesh ref={ref} {...props}>
      <torusKnotGeometry args={[1, 0.35, 220, 32]} />
      <meshStandardMaterial metalness={0.8} roughness={0.2} color="#9b8cff" />
    </mesh>
  );
}

export default function Universe3D() {
  return (
    <div style={{ position: 'relative', height: '80vh', borderRadius: 16, overflow: 'hidden' }}>
      <Canvas camera={{ position: [0, 0, 5], fov: 60 }}>
        <ambientLight intensity={0.6} />
        <directionalLight position={[2, 3, 4]} intensity={1.2} />
        <Stars radius={100} depth={50} count={5000} factor={4} fade />
        <Spinner position={[0, 0, 0]} />
        <OrbitControls enableDamping />
      </Canvas>

      <div style={{
        position: 'absolute', inset: 0, display: 'flex',
        alignItems: 'center', justifyContent: 'center',
        pointerEvents: 'none'
      }}>
        <div style={{ textAlign: 'center' }}>
          <h1 style={{ fontSize: 36, fontWeight: 800 }}>superNova_2177</h1>
          <p style={{ opacity: 0.8 }}>Fork universes. Vote. Build together.</p>
        </div>
      </div>
    </div>
  );
}
