"use client";

import { useEffect, useState } from "react";
import type { Lang, Phase } from "@/lib/roadmap";
import { faNum } from "@/lib/roadmap";

const COPY = {
  fa: {
    kicker: "نقشه‌راه غیررسمی و متن‌باز جامعهٔ فارسی‌زبان",
    h1a: "نقشه‌راه کامل",
    h1b: "باگ‌بانتی",
    lead: "یک برنامهٔ روز‌به‌روز و کاملاً رایگان، از صفر تا شکارچی حرفه‌ای — بر پایهٔ Voorivex، یاشار شاهین‌زاده، PortSwigger Academy و بهترین منابع رایگان جهانی.",
    start: "شروع از روز ۱",
    browse: "مرور همهٔ فازها",
    statusLabel: "$ status",
    days: "روز",
    phases: "فاز",
    hours: "ساعت",
    cost: "هزینه",
    free: "۰",
  },
  en: {
    kicker: "an unofficial, open-source community roadmap",
    h1a: "Complete Bug",
    h1b: "Bounty Roadmap",
    lead: "A precise, day-by-day, completely free program — from zero to professional hunter, built on Voorivex, Yashar Shahinzadeh, PortSwigger Academy, and the best free resources in the world.",
    start: "Start at day 1",
    browse: "Browse all phases",
    statusLabel: "$ status",
    days: "days",
    phases: "phases",
    hours: "hours",
    cost: "cost",
    free: "0",
  },
};

export default function Hero({
  lang,
  phases,
  stats,
  revealed,
}: {
  lang: Lang;
  phases: Phase[];
  stats: { totalDays: number; totalPhases: number; totalHours: number };
  revealed: boolean;
}) {
  const t = COPY[lang];
  const [statRow, setStatRow] = useState(0);

  useEffect(() => {
    if (!revealed) return;
    const timers = [0, 1, 2, 3].map((i) =>
      setTimeout(() => setStatRow(i + 1), 260 + i * 130)
    );
    return () => timers.forEach(clearTimeout);
  }, [revealed]);

  return (
    <section className="relative border-b border-hairline-soft pb-14 pt-6 md:pt-10">
      <div className="grid grid-cols-1 gap-10 md:grid-cols-[auto_1fr_320px] md:gap-8">
        {/* phase rail — real wayfinding, not decoration */}
        <nav
          aria-label={lang === "fa" ? "فازها" : "Phases"}
          className="hidden md:flex flex-col items-center gap-0 pt-3"
        >
          {phases.map((p, i) => (
            <a
              key={p.id}
              href={`#${p.id}`}
              className="group flex flex-col items-center"
              title={p.title}
            >
              <span
                className={`h-2.5 w-2.5 rounded-full border-2 transition-transform group-hover:scale-125 ${
                  i === 0 ? "rail-dot-active" : ""
                }`}
                style={{ borderColor: p.color, background: i === 0 ? p.color : "transparent" }}
              />
              {i < phases.length - 1 && (
                <span className="h-6 w-px bg-hairline" />
              )}
            </a>
          ))}
        </nav>

        {/* headline column */}
        <div className="min-w-0">
          <span className="inline-block rounded-sm border border-hairline bg-void-raised px-3 py-1.5 font-mono-display text-[11px] text-dim">
            {t.kicker}
          </span>
          <h1 className="font-display mt-5 text-[clamp(2.2rem,6vw,4.2rem)] font-medium leading-[1.04] tracking-tight">
            <span className="block text-paper">{t.h1a}</span>
            <span className="block text-signal">{t.h1b}</span>
          </h1>
          <p className="mt-6 max-w-[52ch] text-[1.05rem] leading-8 text-dim">
            {t.lead}
          </p>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <a
              href="#p0"
              className="rounded-sm bg-signal px-6 py-3 text-sm font-semibold text-void transition hover:brightness-110"
            >
              {t.start}
            </a>
            <a
              href="#phase-index"
              className="rounded-sm border border-hairline px-6 py-3 text-sm font-medium text-paper transition hover:border-signal"
            >
              {t.browse}
            </a>
          </div>
        </div>

        {/* terminal stat readout */}
        <div
          dir="ltr"
          className="h-fit rounded-sm border border-hairline bg-void-raised font-mono-display text-[12.5px]"
        >
          <div className="border-b border-hairline px-4 py-2.5 text-dimmer">
            {t.statusLabel}
          </div>
          <dl className="space-y-2 px-4 py-4">
            <Row show={statRow > 0} label={t.days} value={faNum(stats.totalDays, lang)} accent="signal" />
            <Row show={statRow > 1} label={t.phases} value={faNum(stats.totalPhases, lang)} accent="ultraviolet" />
            <Row show={statRow > 2} label={t.hours} value={faNum(stats.totalHours, lang)} accent="signal" />
            <Row show={statRow > 3} label={t.cost} value={`$${t.free}`} accent="phosphor" />
          </dl>
        </div>
      </div>
    </section>
  );
}

function Row({
  show,
  label,
  value,
  accent,
}: {
  show: boolean;
  label: string;
  value: string;
  accent: "signal" | "ultraviolet" | "phosphor";
}) {
  const color =
    accent === "signal" ? "text-signal" : accent === "ultraviolet" ? "text-ultraviolet" : "text-phosphor";
  return (
    <div
      className={`flex items-center justify-between transition-all duration-300 ${
        show ? "translate-y-0 opacity-100" : "translate-y-1 opacity-0"
      }`}
    >
      <dt className="text-dim">{label}</dt>
      <dd className={`font-semibold ${color}`}>{value}</dd>
    </div>
  );
}
