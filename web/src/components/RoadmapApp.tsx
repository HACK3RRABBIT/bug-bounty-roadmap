"use client";

import { useEffect, useMemo, useState } from "react";
import { ROADMAP, totalStats, type Lang } from "@/lib/roadmap";
import BootLoader from "./BootLoader";
import TopBar from "./TopBar";
import Hero from "./Hero";
import RoadmapOverview from "./RoadmapOverview";
import VoorivexCredit from "./VoorivexCredit";
import Controls, { type FilterMode } from "./Controls";
import PhaseSection from "./PhaseSection";

const PROGRESS_KEY = "bbr_progress_v1";

const FOOTER = {
  fa: {
    note: "پیشرفت شما فقط در همین مرورگر (localStorage) ذخیره می‌شود.",
    disclaimer:
      "این یک پروژهٔ غیررسمی و جامعه‌محور است؛ هیچ ارتباط رسمی با Voorivex یا یاشار شاهین‌زاده ندارد.",
    empty: "چیزی با این فیلتر/جست‌وجو پیدا نشد 🕵️",
    reset: "پاک کردن پیشرفت",
    original: "نسخهٔ اصلی سایت",
  },
  en: {
    note: "Your progress is stored only in this browser (localStorage).",
    disclaimer:
      "This is an unofficial, community-built project with no official affiliation to Voorivex or Yashar Shahinzadeh.",
    empty: "Nothing matches this filter/search 🕵️",
    reset: "Reset progress",
    original: "Original site",
  },
};

export default function RoadmapApp() {
  const [lang, setLang] = useState<Lang>("en");
  const [booted, setBooted] = useState(false);
  const [progress, setProgress] = useState<Set<number>>(new Set());
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<FilterMode>("all");
  const [mounted, setMounted] = useState(false);
  const [telegramLinks, setTelegramLinks] = useState<Record<string, { fa?: string; en?: string }>>({});

  useEffect(() => {
    setMounted(true);
    try {
      const raw = localStorage.getItem(PROGRESS_KEY);
      if (raw) setProgress(new Set(JSON.parse(raw)));
    } catch {
      /* ignore */
    }
    // basePath-aware fetch: this file is unversioned and lives in public/,
    // so it can be refreshed independently of a full site rebuild whenever
    // the Telegram channels are re-published.
    const base = (process.env.NEXT_PUBLIC_BASE_PATH || "").replace(/\/$/, "");
    fetch(`${base}/telegram_links.json`)
      .then((r) => (r.ok ? r.json() : {}))
      .then(setTelegramLinks)
      .catch(() => {});
  }, []);

  // Stable per-day deep links (#day-N): scroll to the card once the
  // roadmap has actually rendered (after boot + filters clear it).
  useEffect(() => {
    if (!booted) return;
    const goToHashDay = () => {
      const m = window.location.hash.match(/^#day-(\d+)$/);
      if (!m) return;
      setFilter("all");
      setSearch("");
      // wait a tick for the filter-driven re-render to finish before scrolling
      requestAnimationFrame(() => {
        const el = document.getElementById(`day-${m[1]}`);
        el?.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    };
    goToHashDay();
    window.addEventListener("hashchange", goToHashDay);
    return () => window.removeEventListener("hashchange", goToHashDay);
  }, [booted]);

  function toggleDay(day: number) {
    setProgress((prev) => {
      const next = new Set(prev);
      if (next.has(day)) next.delete(day);
      else next.add(day);
      try {
        localStorage.setItem(PROGRESS_KEY, JSON.stringify([...next]));
      } catch {
        /* ignore */
      }
      return next;
    });
  }

  const roadmap = ROADMAP[lang];
  const stats = useMemo(() => totalStats(lang), [lang]);
  const q = search.trim().toLowerCase();

  function matchesFilter(dayId: number, searchable: string) {
    const isDone = progress.has(dayId);
    if (filter === "done" && !isDone) return false;
    if (filter === "todo" && isDone) return false;
    if (q && !searchable.includes(q)) return false;
    return true;
  }

  const anyVisible = roadmap.phases.some((p) =>
    p.days.some((d) =>
      matchesFilter(d.day, `${d.title} ${d.task} ${d.resources.map((r) => r.t).join(" ")}`.toLowerCase())
    )
  );

  const t = FOOTER[lang];

  return (
    <div dir={lang === "fa" ? "rtl" : "ltr"}>
      {!booted && <BootLoader onDone={() => setBooted(true)} />}

      <div className="mx-auto max-w-6xl px-4">
        <TopBar lang={lang} onLangChange={setLang} />
        <Hero lang={lang} phases={roadmap.phases} stats={stats} revealed={booted} />
        <RoadmapOverview lang={lang} phases={roadmap.phases} progress={progress} />
        <VoorivexCredit lang={lang} />

        <Controls
          lang={lang}
          phases={roadmap.phases}
          search={search}
          onSearch={setSearch}
          filter={filter}
          onFilter={setFilter}
          doneCount={progress.size}
          totalDays={roadmap.generated_days}
        />

        <main>
          {mounted && !anyVisible && (
            <p className="py-20 text-center text-dim">{t.empty}</p>
          )}
          {roadmap.phases.map((p) => (
            <PhaseSection
              key={p.id}
              phase={p}
              lang={lang}
              progress={progress}
              onToggleDay={toggleDay}
              matchesFilter={matchesFilter}
              telegramLinks={telegramLinks}
            />
          ))}
        </main>

        <footer className="mt-14 border-t border-hairline-soft py-10 text-center text-sm text-dim">
          <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-2">
            <a
              href="https://github.com/hack3rrabbit/bug-bounty-roadmap"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-signal"
            >
              GitHub
            </a>
            <span className="text-dimmer">·</span>
            <a
              href="https://hack3rrabbit.github.io/bug-bounty-roadmap/"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-signal"
            >
              {t.original}
            </a>
            <span className="text-dimmer">·</span>
            <span>{t.note}</span>
            <span className="text-dimmer">·</span>
            <button
              onClick={() => {
                if (confirm(lang === "fa" ? "مطمئنی؟" : "Are you sure?")) {
                  setProgress(new Set());
                  try {
                    localStorage.removeItem(PROGRESS_KEY);
                  } catch {
                    /* ignore */
                  }
                }
              }}
              className="hover:text-crimson"
            >
              {t.reset}
            </button>
          </div>
          <p className="mt-4 text-xs text-dimmer">{t.disclaimer}</p>
        </footer>
      </div>
    </div>
  );
}
