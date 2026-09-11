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

  return (
    <section className="border-b border-hairline-soft py-12">
      <h2 className="font-display text-xl font-medium">{t.title}</h2>
      <p className="mt-1.5 text-sm text-dim">{t.sub}</p>

      <div className="mt-7 grid grid-cols-1 gap-px overflow-hidden rounded-sm border border-hairline bg-hairline sm:grid-cols-2 lg:grid-cols-3">
        {phases.map((p, i) => {
          const done = p.days.filter((d) => progress.has(d.day)).length;
          const pct = p.days.length ? Math.round((done / p.days.length) * 100) : 0;
          return (
            <a
              key={p.id}
              href={`#${p.id}`}
              className="bracket flex flex-col gap-2 bg-void px-4 py-3.5 transition-colors hover:bg-void-raised-2"
            >
              <div className="flex items-center gap-2 text-dimmer">
                <span className="font-mono-display text-[11px]">{faNum(i, lang)}</span>
                <span className="h-1.5 w-1.5 rounded-full" style={{ background: p.color }} />
                <span className="text-base leading-none">{p.icon}</span>
              </div>
              <div className="text-[0.85rem] font-medium leading-snug text-paper">{p.title}</div>
              <div className="flex items-center justify-between font-mono-display text-[10px] text-dimmer">
                <span>{faNum(p.days.length, lang)} {t.days}</span>
                <span>{faNum(pct, lang)}%</span>
              </div>
              <div className="h-px overflow-hidden bg-hairline">
                <div className="h-full bg-paper transition-all" style={{ width: `${pct}%` }} />
              </div>
            </a>
          );
        })}
      </div>
    </section>
  );
}
