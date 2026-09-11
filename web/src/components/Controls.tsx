"use client";

import type { Lang, Phase } from "@/lib/roadmap";
import { faNum } from "@/lib/roadmap";

export type FilterMode = "all" | "todo" | "done";

const COPY = {
  fa: {
    search: "جست‌وجو در عنوان، توضیح یا منابع روزها...",
    all: "همه",
    todo: "باقی‌مانده",
    done: "انجام‌شده",
  },
  en: {
    search: "Search titles, descriptions, or resources...",
    all: "All",
    todo: "Remaining",
    done: "Done",
  },
};

export default function Controls({
  lang,
  phases,
  search,
  onSearch,
  filter,
  onFilter,
  doneCount,
  totalDays,
}: {
  lang: Lang;
  phases: Phase[];
  search: string;
  onSearch: (v: string) => void;
  filter: FilterMode;
  onFilter: (f: FilterMode) => void;
  doneCount: number;
  totalDays: number;
}) {
  const t = COPY[lang];
  const pct = totalDays ? Math.round((doneCount / totalDays) * 100) : 0;

  return (
    <div id="phase-index" className="sticky top-0 z-40 -mx-4 scroll-mt-4 border-b border-hairline-soft bg-void px-4 py-3.5">
      <div className="flex flex-wrap items-center gap-2.5">
        <input
          value={search}
          onChange={(e) => onSearch(e.target.value)}
          placeholder={t.search}
          className="min-w-[220px] flex-1 rounded-sm border border-hairline bg-void-raised px-3.5 py-2.5 text-sm text-paper placeholder:text-dimmer focus:border-signal focus:outline-none"
        />
        {(["all", "todo", "done"] as FilterMode[]).map((f) => (
          <button
            key={f}
            onClick={() => onFilter(f)}
            className={`rounded-sm border px-3.5 py-2.5 text-sm transition ${
              filter === f
                ? "border-signal bg-signal text-void font-semibold"
                : "border-hairline text-dim hover:text-paper"
            }`}
          >
            {t[f]}
          </button>
        ))}
        <div className="flex min-w-[150px] items-center gap-2">
          <div className="h-px flex-1 bg-hairline">
            <div
              className="h-full bg-paper transition-all"
              style={{ width: `${pct}%` }}
            />
          </div>
          <span className="font-mono-display text-xs text-dimmer whitespace-nowrap">
            {faNum(pct, lang)}%
          </span>
        </div>
      </div>

      <div className="mt-3 flex gap-2 overflow-x-auto pb-1">
        {phases.map((p) => (
          <a
            key={p.id}
            href={`#${p.id}`}
            className="flex-none whitespace-nowrap rounded-sm border border-hairline px-3 py-1.5 text-xs text-dim transition hover:border-signal hover:text-paper"
          >
            {p.icon} {p.title}
          </a>
        ))}
      </div>
    </div>
  );
}
