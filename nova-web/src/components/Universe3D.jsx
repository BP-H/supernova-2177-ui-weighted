"use client";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Stars } from "@react-three/drei";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import * as THREE from "three";

function Node({ position, label, votes }) {
  const totalVotes = Object.values(votes || {}).reduce((a,b) => a+b, 0);
  const size = 0.5 + totalVotes * 0.05;
  const color = votes.human > votes.company ? "hotpink" : "skyblue";
  return (
    <mesh position={position}>
      <sphereGeometry args={[size, 32, 32]} />
      <meshStandardMaterial emissive={color} emissiveIntensity={0.6} color={color} />
    </mesh>
  );
}

function Link({ start, end }) {
  const points = [start, end];
  const curve = new THREE.CatmullRomCurve3(points.map(p => new THREE.Vector3(...p)));
  const geometry = new THREE.TubeGeometry(curve, 20, 0.02, 8, false);
  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial emissive={"#999"} emissiveIntensity={0.3} color={"#666"} />
    </mesh>
  );
}

export default function Universe3D() {
  const [data, setData] = useState({nodes:[], links:[]});

  useEffect(() => {
    async function fetchData() {
      const res = await api("/universe");
      const json = await res.json();
      setData(json);
    }
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const positions = {};
  data.nodes.forEach((n,i) => {
    positions[n.id] = [
      Math.sin(i) * 5,
      Math.cos(i) * 5,
      (i % 3) * 2 - 3
    ];
  });

  return (
    <Canvas camera={{ position: [0, 0, 15], fov: 50 }}>
      <ambientLight intensity={0.4} />
      <pointLight position={[10, 10, 10]} />
      <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade />
      {data.nodes.map(n => (
        <Node key={n.id} position={positions[n.id]} label={n.label} votes={n.votes} />
      ))}
      {data.links.map((l, i) => (
        <Link key={i} start={positions[l.source]} end={positions[l.target]} />
      ))}
      <OrbitControls enablePan={true} enableZoom={true} />
    </Canvas>
  );
}
