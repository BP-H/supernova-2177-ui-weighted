/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    // Allow our external image hosts used across the app
    remotePatterns: [
      { protocol: 'https', hostname: 'images.unsplash.com' },
      { protocol: 'https', hostname: 'picsum.photos' },
      { protocol: 'https', hostname: 'api.dicebear.com' },
      { protocol: 'https', hostname: 'placehold.co' }, // used in Shell cover
    ],
    // DiceBear avatars are SVGs; allow them
    dangerouslyAllowSVG: true,
    // Optional: slightly smaller payloads on modern browsers
    formats: ['image/avif', 'image/webp'],
  },
};

module.exports = nextConfig;
