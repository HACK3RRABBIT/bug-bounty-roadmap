"use client";

import { useEffect, useRef, useState } from "react";

// The boot sequence is always rendered in English, regardless of site
// language — it's a terminal-culture flourish, not localized UI copy.
const BOOT_LINES = [
  "$ connecting to voorivex-academy ... OK",
  "$ mounting portswigger-academy ... OK",
  "$ decrypting 141 training modules ... OK",
  "$ verifying 181 free resources ... OK",
  "$ initializing hunter environment ...",
  "> connection established.",
];

const CHARS_PER_SECOND = 90; // time-based reveal rate, immune to per-render cost
const LINE_PAUSE_MS = 90;
const HOLD_AFTER_MS = 500;

export default function BootLoader({ onDone }: { onDone: () => void }) {
  const [visibleLines, setVisibleLines] = useState<string[]>([]);
  const [activeLine, setActiveLine] = useState(0);
  const [exiting, setExiting] = useState(false);
  const doneRef = useRef(false);

  useEffect(() => {
    function finish() {
      if (doneRef.current) return;
      doneRef.current = true;
      setExiting(true);
      setTimeout(onDone, 380);
    }

    const reduceMotion =
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (reduceMotion) {
      finish();
      return;
    }

    let raf = 0;
    let lineIdx = 0;
    let lineStart = performance.now();
    let cancelled = false;

    function tick(now: number) {
      if (cancelled) return;
      const line = BOOT_LINES[lineIdx];
      const elapsed = now - lineStart;
      const charsShown = Math.max(
        0,
        Math.min(line.length, Math.floor((elapsed / 1000) * CHARS_PER_SECOND))
      );
      setVisibleLines((prev) => {
        const next = [...prev];
        next[lineIdx] = line.slice(0, charsShown);
        return next;
      });
      setActiveLine(lineIdx);

      if (charsShown >= line.length) {
        if (lineIdx < BOOT_LINES.length - 1) {
          lineIdx++;
          lineStart = now + LINE_PAUSE_MS;
          raf = requestAnimationFrame(tick);
        } else {
          setTimeout(finish, HOLD_AFTER_MS);
        }
        return;
      }
      raf = requestAnimationFrame(tick);
    }

    raf = requestAnimationFrame(tick);

    function skip() {
      cancelled = true;
      cancelAnimationFrame(raf);
      finish();
    }
    window.addEventListener("keydown", skip);
    window.addEventListener("click", skip);

    return () => {
      cancelled = true;
      cancelAnimationFrame(raf);
      window.removeEventListener("keydown", skip);
      window.removeEventListener("click", skip);
    };
    // run once on mount only — onDone is stable enough for this one-shot sequence
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div
      className={`fixed inset-0 z-[100] flex items-center justify-center bg-void transition-opacity duration-[380ms] ${
        exiting ? "opacity-0 pointer-events-none" : "opacity-100"
      }`}
      aria-hidden={exiting}
    >
      <div className="scanline-fade absolute inset-0" />
      <div
        dir="ltr"
        className="relative w-[min(92vw,560px)] rounded-sm border border-hairline bg-void-raised p-5 font-mono-display text-[13px] leading-relaxed text-phosphor shadow-[0_0_60px_rgba(57,255,140,0.08)]"
      >
        {BOOT_LINES.map((_, i) => (
          <div key={i} className="min-h-[1.4em] whitespace-pre">
            {visibleLines[i]}
            {i === activeLine && <span className="cursor-blink">▌</span>}
          </div>
        ))}
      </div>
      <p className="absolute bottom-8 text-[11px] text-dimmer font-mono-display">
        click to skip
      </p>
    </div>
  );
}
