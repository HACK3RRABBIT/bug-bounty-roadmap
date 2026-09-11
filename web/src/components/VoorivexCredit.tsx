"use client";

import Image from "next/image";
import { BASE_PATH, type Lang } from "@/lib/roadmap";

const COPY = {
  fa: {
    kicker: "منبع اصلی",
    title: "کلاس‌های آکادمی Voorivex",
    body: "این نقشه‌راه بر پایهٔ ساختار و متدولوژی آکادمی Voorivex و آموزش‌های رایگان یاشار شاهین‌زاده بنا شده. کلاس‌های رسمی آکادمی (OWASP Zero و نسخه‌های بعدی آن) پولی‌اند — تصویر زیر فقط برای آشنایی با ساختار دوره‌هاست، نه دعوت به ثبت‌نام.",
    cta: "مشاهدهٔ آکادمی Voorivex",
  },
  en: {
    kicker: "primary source",
    title: "Voorivex Academy classes",
    body: "This roadmap is built on the structure and methodology of Voorivex Academy and Yashar Shahinzadeh's free teachings. The academy's official classes (OWASP Zero and its later versions) are paid — the image below is shown only to illustrate the course structure, not as an invitation to enroll.",
    cta: "Visit Voorivex Academy",
  },
};

export default function VoorivexCredit({ lang }: { lang: Lang }) {
  const t = COPY[lang];
  return (
    <section className="border-b border-hairline-soft py-12">
      <div className="grid grid-cols-1 gap-8 md:grid-cols-2 md:items-center">
        <div>
          <h2 className="font-display text-xl font-medium">{t.title}</h2>
          <p className="mt-3 max-w-[46ch] text-sm leading-7 text-dim">{t.body}</p>
          <a
            href="https://voorivex.academy/classes"
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-block text-sm text-signal underline decoration-signal/30 underline-offset-4 hover:decoration-signal"
          >
            {t.cta} ↗
          </a>
        </div>
        <a
          href="https://voorivex.academy/classes"
          target="_blank"
          rel="noopener noreferrer"
          className="bracket block overflow-hidden rounded-sm border border-hairline"
        >
          <Image
            src={`${BASE_PATH}/voorivex-classes.jpg`}
            alt="Voorivex Academy class listing (OWASP Zero series)"
            width={1506}
            height={812}
            className="w-full opacity-90 transition hover:opacity-100"
          />
        </a>
      </div>
    </section>
  );
}
