import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  typescript: {
    // Temporarily disable TypeScript errors during build
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
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
  async rewrites() {
    return [
      {
        source: '/docs/:path*',
        destination: 'https://slag.gitbook.io/:path*', // Replace with your GitBook URL
      },
    ];
  },
};

export default nextConfig;
