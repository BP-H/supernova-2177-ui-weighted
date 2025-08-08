'use client';
import { useEffect } from 'react';
import * as THREE from 'three';

export default function Universe3D() {
  useEffect(() => {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Add some glowing spheres (nodes)
    const geometry = new THREE.SphereGeometry(0.5, 32, 32);
    const material = new THREE.MeshStandardMaterial({ color: 0xff5500, emissive: 0xff2200 });
    for (let i = 0; i < 15; i++) {
      const sphere = new THREE.Mesh(geometry, material);
      sphere.position.set(Math.random()*10-5, Math.random()*10-5, Math.random()*10-5);
      scene.add(sphere);
    }

    const light = new THREE.PointLight(0xffffff, 1);
    light.position.set(5,5,5);
    scene.add(light);

    camera.position.z = 10;
    const animate = () => { requestAnimationFrame(animate); renderer.render(scene, camera); };
    animate();
  }, []);

  return null;
}
