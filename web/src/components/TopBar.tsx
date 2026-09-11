"use client";

import Image from "next/image";
import type { Lang } from "@/lib/roadmap";

export default function TopBar({
  lang,
  onLangChange,
}: {
  lang: Lang;
  onLangChange: (l: Lang) => void;
}) {
  return (
    <header className="flex items-center justify-between py-4">
      <a href="#" className="flex items-center gap-2.5 font-mono-display text-sm font-medium">
        <Image src="/logo.svg" alt="" width={26} height={26} priority />
        <span>{lang === "fa" ? "نقشه‌راه باگ‌بانتی" : "Bug Bounty Roadmap"}</span>
      </a>
      <div className="flex items-center gap-2">
        <button
          onClick={() => onLangChange(lang === "fa" ? "en" : "fa")}
          className="rounded-sm border border-hairline px-3 py-1.5 font-mono-display text-xs text-dim transition hover:border-signal hover:text-paper"
        >
          {lang === "fa" ? "EN" : "FA"}
        </button>
        <a
          href="https://github.com/hack3rrabbit/bug-bounty-roadmap"
          target="_blank"
          rel="noopener noreferrer"
          className="rounded-sm border border-hairline px-3 py-1.5 font-mono-display text-xs text-dim transition hover:border-signal hover:text-paper"
        >
          GitHub
        </a>
      </div>
    </header>
  );
}
