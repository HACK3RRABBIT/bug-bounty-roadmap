import type { NextConfig } from "next";

// Set BASE_PATH when building for a subpath deployment (e.g. GitHub Pages at
// /bug-bounty-roadmap/v2). Leave unset for the local systemd-served build,
// which is served from the origin root.
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || "";

const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
  trailingSlash: true,
  basePath: basePath || undefined,
  assetPrefix: basePath || undefined,
};

export default nextConfig;
