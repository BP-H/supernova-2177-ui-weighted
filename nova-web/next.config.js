/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['api.dicebear.com', 'picsum.photos', 'placehold.co'],
  },
};

module.exports = nextConfig;
