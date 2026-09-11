"use client";

import type { Day, Lang } from "@/lib/roadmap";
import { KIND_LABEL, faNum } from "@/lib/roadmap";

const KIND_STYLES: Record<Day["kind"], string> = {
  learn: "bg-ultraviolet/15 text-ultraviolet",
  practice: "bg-signal/15 text-signal",
  review: "bg-amber/15 text-amber",
  milestone: "bg-phosphor/15 text-phosphor",
};

export default function DayCard({
  day,
  lang,
  phaseColor,
  done,
  onToggle,
}: {
  day: Day;
  lang: Lang;
  phaseColor: string;
  done: boolean;
  onToggle: () => void;
}) {
  return (
    <div
      className="bracket flex flex-col gap-3 rounded-sm border border-hairline bg-void-raised p-5 transition-colors hover:border-hairline"
      style={{ borderInlineStartWidth: 3, borderInlineStartColor: phaseColor }}
    >
      <div className="flex items-center justify-between gap-2">
        <span
          className="font-mono-display text-xs font-semibold"
          style={{ color: phaseColor }}
        >
          {lang === "fa" ? "روز" : "Day"} {faNum(day.day, lang)}
        </span>
        <span className={`rounded-sm px-2 py-0.5 text-[11px] font-medium ${KIND_STYLES[day.kind]}`}>
          {KIND_LABEL[lang][day.kind]}
        </span>
      </div>

      <h3 className={`font-semibold text-[0.97rem] ${done ? "text-dim line-through decoration-phosphor/60" : "text-paper"}`}>
        {day.title}
      </h3>
      <p className="text-[0.86rem] leading-6 text-dim">{day.task}</p>

      <div className="flex flex-col gap-1.5">
        {day.resources.map((r) => (
          <a
            key={r.u}
            href={r.u}
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-sm border border-hairline-soft bg-void px-2.5 py-1.5 text-[0.78rem] text-dim transition hover:border-signal hover:text-signal"
          >
            ↗ {r.t}
          </a>
        ))}
      </div>

      <div className="mt-auto flex items-center justify-between pt-1 font-mono-display text-[0.74rem] text-dimmer">
        <span>⏱ {faNum(day.hours, lang)}{lang === "fa" ? " ساعت تخمینی" : "h estimated"}</span>
        <label className="flex cursor-pointer items-center gap-1.5 text-dim">
          <input
            type="checkbox"
            checked={done}
            onChange={onToggle}
            className="h-3.5 w-3.5 accent-phosphor"
          />
          {lang === "fa" ? "انجام شد" : "Done"}
        </label>
      </div>
    </div>
  );
}
