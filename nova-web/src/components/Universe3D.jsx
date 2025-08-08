"use client";
import React from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Stars } from "@react-three/drei";

export default function Universe3D() {
  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <Canvas camera={{ position: [0, 0, 5], fov: 75 }}>
        {/* Space background */}
        <color attach="background" args={["#000010"]} />
        <Stars radius={300} depth={60} count={5000} factor={7} fade />
        
        {/* Example spinning planet */}
        <mesh rotation={[0.4, 0.2, 0]}>
          <sphereGeometry args={[1, 32, 32]} />
          <meshStandardMaterial color="orange" wireframe />
        </mesh>

        {/* Lights */}
        <ambientLight intensity={0.5} />
        <pointLight position={[5, 5, 5]} intensity={2} />

        {/* Controls */}
        <OrbitControls enableZoom={true} />
      </Canvas>
    </div>
  );
}
