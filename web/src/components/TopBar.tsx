"use client";

import Image from "next/image";
import { BASE_PATH, type Lang } from "@/lib/roadmap";

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
        <Image src={`${BASE_PATH}/logo.svg`} alt="" width={26} height={26} priority />
        <span>{lang === "fa" ? "نقشه‌راه باگ‌بانتی" : "Bug Bounty Roadmap"}</span>
      </a>
      <div className="flex items-center gap-5 text-sm">
        <button
          onClick={() => onLangChange(lang === "fa" ? "en" : "fa")}
          className="font-mono-display text-xs text-dim transition hover:text-signal"
        >
          {lang === "fa" ? "EN" : "FA"}
        </button>
        <a href="../" className="text-dim transition hover:text-signal">
          {lang === "fa" ? "نسخهٔ کلاسیک" : "Classic version"}
        </a>
        <a
          href="https://github.com/hack3rrabbit/bug-bounty-roadmap"
          target="_blank"
          rel="noopener noreferrer"
          className="text-dim transition hover:text-signal"
        >
          GitHub
        </a>
      </div>
    </header>
  );
}
