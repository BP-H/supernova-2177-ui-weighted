import React, { useState, useRef, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Environment, Line, Html, useGLTF } from '@react-three/drei';
import { useSpring, animated } from '@react-spring/three';

// A reusable component for a glowing sphere navigation point.
const NavPoint = ({ position, name, color, onClick, ...props }) => {
  const mesh = useRef();
  const [hovered, setHover] = useState(false);
  const [clicked, setClick] = useState(false);

  // Smooth scale animation on click.
  const { scale } = useSpring({ scale: clicked ? 1.5 : 1 });

  // Make the sphere spin on every frame.
  useFrame(() => (mesh.current.rotation.y += 0.005));

  return (
    <animated.mesh
      {...props}
      ref={mesh}
      position={position}
      scale={scale}
      onPointerOver={() => setHover(true)}
      onPointerOut={() => setHover(false)}
      onClick={(e) => {
        setClick(!clicked);
        onClick(e, position);
      }}
    >
      <sphereGeometry args={[0.3, 32, 32]} />
      <meshStandardMaterial
        color={hovered ? 'cyan' : color}
        emissive={hovered ? 'cyan' : color}
        emissiveIntensity={clicked ? 1.5 : 0.5}
      />
      <Html distanceFactor={10}>
        <div className="text-white text-xs font-mono select-none" style={{ transform: 'translate3d(-50%,-50%,0)' }}>
          {name}
        </div>
      </Html>
    </animated.mesh>
  );
};

// A component that loads a 3D model.
const FuturisticShip = (props) => {
  // Replace this URL with the path to your own .gltf or .glb file.
  const { scene } = useGLTF('https://vazg.com/gltf/pbr/Spaceship/glTF-Embedded/Spaceship.gltf');
  return <primitive object={scene} {...props} />;
};

// This is the entire 3D scene, which includes the Canvas.
export default function Scene({ cameraPosition, path, handleNavClick }) {
  return (
    <Canvas
      camera={{ position: cameraPosition, fov: 60 }}
      style={{ width: '100vw', height: '100vh' }}
      onCreated={({ gl }) => {
        gl.setClearColor('#0a0a0c');
      }}
    >
      <Suspense fallback={null}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1} color="magenta" />
        <directionalLight position={[-10, -10, -5]} intensity={0.8} color="cyan" />
        <Environment preset="night" />

        <group position={[0, 0, 0]}>
          <NavPoint position={[0, 0, 0]} name="Home Base" color="white" onClick={handleNavClick} />
          <NavPoint position={[5, 5, -5]} name="Sector Alpha" color="magenta" onClick={handleNavClick} />
          <NavPoint position={[-8, 3, 2]} name="Nebula Point" color="cyan" onClick={handleNavClick} />
          <NavPoint position={[3, -6, 8]} name="Asteroid Belt" color="lime" onClick={handleNavClick} />

          <Line
              points={path}
              color="yellow"
              lineWidth={3}
              dashed={false}
          />

          <mesh position={[-5, -5, -5]}>
            <boxGeometry args={[1, 1, 1]} />
            <meshStandardMaterial color="purple" emissive="purple" emissiveIntensity={0.8} />
          </mesh>

          <FuturisticShip position={[-20, 20, -20]} scale={20} />
        </group>

        <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
      </Suspense>
    </Canvas>
  );
}

useGLTF.preload('https://vazg.com/gltf/pbr/Spaceship/glTF-Embedded/Spaceship.gltf');
