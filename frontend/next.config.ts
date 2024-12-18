import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      }
    ],
    unoptimized: false,
    domains: ['vercel.app', 'localhost']
  },
  experimental: {
    appDir: true
  }
};

export default nextConfig;
