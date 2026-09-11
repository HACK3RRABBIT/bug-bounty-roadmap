"use client";

import type { Lang, Phase } from "@/lib/roadmap";
import { faNum } from "@/lib/roadmap";

const COPY = {
  fa: { title: "نقشهٔ کلی مسیر", sub: "قبل از جزئیات، کل مسیر را یک نگاه ببین — روی هر گره کلیک کن.", days: "روز" },
  en: { title: "The roadmap at a glance", sub: "See the whole path before the details — click any node to jump in.", days: "days" },
};

export default function RoadmapOverview({
  lang,
  phases,
  progress,
}: {
  lang: Lang;
  phases: Phase[];
  progress: Set<number>;
}) {
  const t = COPY[lang];
  const arrow = lang === "fa" ? "←" : "→";

  return (
    <section className="border-b border-hairline-soft py-12">
      <h2 className="font-display text-xl font-medium">{t.title}</h2>
      <p className="mt-1.5 text-sm text-dim">{t.sub}</p>

      <div className="mt-7 flex flex-wrap items-center gap-x-1 gap-y-5">
        {phases.map((p, i) => {
          const done = p.days.filter((d) => progress.has(d.day)).length;
          const pct = p.days.length ? Math.round((done / p.days.length) * 100) : 0;
          return (
            <div key={p.id} className="flex items-center gap-1">
              <a
                href={`#${p.id}`}
                className="bracket group flex w-[168px] flex-col gap-2 rounded-sm border bg-void-raised px-3.5 py-3 transition-transform hover:-translate-y-0.5"
                style={{ borderColor: "var(--hairline)" }}
              >
                <div className="flex items-center gap-2">
                  <span
                    className="flex h-6 w-6 flex-none items-center justify-center rounded-sm font-mono-display text-[10px] font-bold"
                    style={{ background: `${p.color}22`, color: p.color }}
                  >
                    {faNum(i, lang)}
                  </span>
                  <span className="text-base leading-none">{p.icon}</span>
                </div>
                <div className="text-[0.82rem] font-medium leading-snug text-paper">{p.title}</div>
                <div className="flex items-center justify-between">
                  <span className="font-mono-display text-[10px] text-dimmer">
                    {faNum(p.days.length, lang)} {t.days}
                  </span>
                  <span className="font-mono-display text-[10px]" style={{ color: p.color }}>
                    {faNum(pct, lang)}%
                  </span>
                </div>
                <div className="h-1 overflow-hidden rounded-full bg-void-raised-2">
                  <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: p.color }} />
                </div>
              </a>
              {i < phases.length - 1 && (
                <span className="hidden font-mono-display text-dimmer sm:inline">{arrow}</span>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
