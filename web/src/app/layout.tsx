import type { Metadata } from "next";
import { IBM_Plex_Mono, Inter, Vazirmatn } from "next/font/google";
import "./globals.css";

const plexMono = IBM_Plex_Mono({
  variable: "--font-plex-mono",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

const vazirmatn = Vazirmatn({
  variable: "--font-vazirmatn",
  subsets: ["arabic", "latin"],
  weight: ["400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: "Complete Bug Bounty Roadmap | نقشه‌راه کامل باگ‌بانتی",
  description:
    "A precise, 100% free, day-by-day roadmap from zero to professional bug bounty hunter — in Persian and English.",
  icons: {
    icon: [
      { url: "/logo.svg", type: "image/svg+xml" },
      { url: "/favicon-32.png", sizes: "32x32", type: "image/png" },
    ],
    apple: "/apple-touch-icon.png",
  },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${plexMono.variable} ${inter.variable} ${vazirmatn.variable} h-full`}
      suppressHydrationWarning
    >
      <body className="min-h-full bg-void text-paper" suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
