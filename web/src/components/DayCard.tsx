"use client";

import type { Day, Lang } from "@/lib/roadmap";
import { KIND_LABEL, faNum } from "@/lib/roadmap";

export default function DayCard({
  day,
  lang,
  done,
  onToggle,
}: {
  day: Day;
  lang: Lang;
  done: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="flex flex-col gap-2.5 border-b border-hairline-soft py-5 first:pt-0 last:border-b-0">
      <div className="flex flex-wrap items-center gap-3 font-mono-display text-[11px] text-dimmer">
        <span>{lang === "fa" ? "روز" : "Day"} {faNum(day.day, lang)}</span>
        <span className="h-1 w-1 rounded-full bg-hairline" />
        <span>{KIND_LABEL[lang][day.kind]}</span>
        <span className="h-1 w-1 rounded-full bg-hairline" />
        <span>{faNum(day.hours, lang)}{lang === "fa" ? " ساعت تخمینی" : "h estimated"}</span>
        <label className="ms-auto flex cursor-pointer items-center gap-1.5 text-dim">
          <input type="checkbox" checked={done} onChange={onToggle} className="h-3.5 w-3.5 accent-paper" />
          {lang === "fa" ? "انجام شد" : "Done"}
        </label>
      </div>

      <h3 className={`text-[0.98rem] font-medium ${done ? "text-dim line-through" : "text-paper"}`}>
        {day.title}
      </h3>
      <p className="text-[0.86rem] leading-7 text-dim">{day.task}</p>

      <div className="flex flex-wrap gap-x-4 gap-y-1.5">
        {day.resources.map((r) => (
          <a
            key={r.u}
            href={r.u}
            target="_blank"
            rel="noopener noreferrer"
            className="text-[0.8rem] text-signal underline decoration-signal/30 underline-offset-4 hover:decoration-signal"
          >
            {r.t} ↗
          </a>
        ))}
      </div>
    </div>
  );
}
