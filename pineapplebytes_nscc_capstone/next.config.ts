<<<<<<< HEAD
﻿/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
=======
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49
}

module.exports = nextConfig
