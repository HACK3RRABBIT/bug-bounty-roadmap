import roadmapFa from "@/data/roadmap.fa.json";
import roadmapEn from "@/data/roadmap.en.json";
import changelogData from "@/data/changelog.json";

export type Kind = "learn" | "practice" | "review" | "milestone";

export type Resource = { t: string; u: string };

export type Day = {
  day: number;
  title: string;
  task: string;
  resources: Resource[];
  hours: number;
  kind: Kind;
};

export type Phase = {
  id: string;
  title: string;
  subtitle: string;
  icon: string;
  color: string;
  days: Day[];
};

export type Roadmap = {
  generated_days: number;
  phases: Phase[];
};

export type ChangelogItem = {
  id: number;
  date: string;
  title_fa: string;
  body_fa: string;
  title_en: string;
  body_en: string;
};

export type Lang = "fa" | "en";

export const ROADMAP: Record<Lang, Roadmap> = {
  fa: roadmapFa as Roadmap,
  en: roadmapEn as Roadmap,
};

export const CHANGELOG = changelogData as ChangelogItem[];

export function allDays(lang: Lang) {
  return ROADMAP[lang].phases.flatMap((p) =>
    p.days.map((d) => ({ ...d, phaseId: p.id, phaseColor: p.color, phaseTitle: p.title }))
  );
}

export function totalStats(lang: Lang) {
  const days = allDays(lang);
  const totalHours = days.reduce((s, d) => s + d.hours, 0);
  const uniqueResources = new Set(days.flatMap((d) => d.resources.map((r) => r.u))).size;
  return {
    totalDays: ROADMAP[lang].generated_days,
    totalPhases: ROADMAP[lang].phases.length,
    totalHours: Math.round(totalHours),
    uniqueResources,
    months: Math.round(((ROADMAP[lang].generated_days / 6) * 7) / 30 * 10) / 10,
  };
}

export const KIND_LABEL: Record<Lang, Record<Kind, string>> = {
  fa: { learn: "آموزش", practice: "تمرین عملی", review: "مرور", milestone: "نقطهٔ عطف" },
  en: { learn: "Learn", practice: "Hands-on", review: "Review", milestone: "Milestone" },
};

const FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
export function faNum(n: number | string, lang: Lang): string {
  const s = String(n);
  if (lang !== "fa") return s;
  return s.replace(/[0-9]/g, (d) => FA_DIGITS[Number(d)]);
}
