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
}: {
  phase: Phase;
  lang: Lang;
  progress: Set<number>;
  onToggleDay: (day: number) => void;
  matchesFilter: (dayId: number, searchable: string) => boolean;
}) {
  const doneCount = phase.days.filter((d) => progress.has(d.day)).length;
  const pct = phase.days.length ? Math.round((doneCount / phase.days.length) * 100) : 0;

  const visibleDays = phase.days.filter((d) =>
    matchesFilter(d.day, `${d.title} ${d.task} ${d.resources.map((r) => r.t).join(" ")}`.toLowerCase())
  );

  if (visibleDays.length === 0) return null;

  return (
    <section id={phase.id} className="scroll-mt-28 py-10">
      <div
        className="flex items-center gap-3.5"
        style={{ borderInlineStart: `3px solid ${phase.color}`, paddingInlineStart: 16 }}
      >
        <span className="text-2xl leading-none">{phase.icon}</span>
        <div>
          <h2 className="text-lg font-semibold">{phase.title}</h2>
          <p className="text-sm text-dim">{phase.subtitle}</p>
        </div>
      </div>

      <div
        className="mt-3 flex items-center gap-3"
        style={{ paddingInlineStart: 19 }}
      >
        <div className="h-1.5 max-w-[220px] flex-1 overflow-hidden rounded-full bg-void-raised-2">
          <div
            className="h-full rounded-full transition-all"
            style={{ width: `${pct}%`, background: phase.color }}
          />
        </div>
        <span className="font-mono-display text-xs text-dimmer">
          {faNum(doneCount, lang)}/{faNum(phase.days.length, lang)} {lang === "fa" ? "روز" : "days"}
        </span>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {visibleDays.map((d) => (
          <DayCard
            key={d.day}
            day={d}
            lang={lang}
            phaseColor={phase.color}
            done={progress.has(d.day)}
            onToggle={() => onToggleDay(d.day)}
          />
        ))}
      </div>
    </section>
  );
}
