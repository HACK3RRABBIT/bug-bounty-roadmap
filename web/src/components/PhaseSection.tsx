"use client";

import type { Phase, Lang } from "@/lib/roadmap";
import { faNum } from "@/lib/roadmap";
import DayCard from "./DayCard";

export default function PhaseSection({
  phase,
  lang,
  progress,
  onToggleDay,
  matchesFilter,
  telegramLinks,
}: {
  phase: Phase;
  lang: Lang;
  progress: Set<number>;
  onToggleDay: (day: number) => void;
  matchesFilter: (dayId: number, searchable: string) => boolean;
  telegramLinks?: Record<string, { fa?: string; en?: string }>;
}) {
  const doneCount = phase.days.filter((d) => progress.has(d.day)).length;
  const pct = phase.days.length ? Math.round((doneCount / phase.days.length) * 100) : 0;

  const visibleDays = phase.days.filter((d) =>
    matchesFilter(d.day, `${d.title} ${d.task} ${d.resources.map((r) => r.t).join(" ")}`.toLowerCase())
  );

  if (visibleDays.length === 0) return null;

  return (
    <section id={phase.id} className="scroll-mt-28 border-b border-hairline-soft py-10">
      <div className="flex items-center gap-3">
        <span className="text-xl leading-none">{phase.icon}</span>
        <div>
          <h2 className="text-lg font-medium">{phase.title}</h2>
          <p className="text-sm text-dim">{phase.subtitle}</p>
        </div>
      </div>

      <div className="mt-3 flex items-center gap-3">
        <div className="h-px max-w-[220px] flex-1 bg-hairline">
          <div className="h-full bg-paper" style={{ width: `${pct}%` }} />
        </div>
        <span className="font-mono-display text-xs text-dimmer">
          {faNum(doneCount, lang)}/{faNum(phase.days.length, lang)} {lang === "fa" ? "روز" : "days"}
        </span>
      </div>

      <div className="mt-6">
        {visibleDays.map((d) => (
          <DayCard
            key={d.day}
            day={d}
            lang={lang}
            done={progress.has(d.day)}
            onToggle={() => onToggleDay(d.day)}
            telegramUrl={telegramLinks?.[String(d.day)]?.[lang]}
          />
        ))}
      </div>
    </section>
  );
}
