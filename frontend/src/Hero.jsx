import React from 'react';
import CommandInput from './CommandInput';
import ExamplePrompts from './ExamplePrompts';
import { Sparkles, ShieldCheck, Zap } from 'lucide-react';

export default function Hero({ onSubmitGoal }) {
  return (
    <section className="relative flex min-h-[calc(100vh-4rem)] flex-col items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
      
      {/* Background Subtle Ambience */}
      <div className="pointer-events-none absolute inset-0 -z-10 flex items-center justify-center overflow-hidden">
        <div className="h-[480px] w-[640px] rounded-full bg-gradient-to-tr from-neutral-200/40 via-neutral-100/20 to-transparent blur-3xl opacity-60" />
      </div>

      <div className="w-full max-w-4xl text-center">
        
        {/* Eyebrow badge */}
        <div className="inline-flex items-center gap-2 rounded-full border border-neutral-200/80 bg-white/80 px-3 py-1 text-xs font-medium text-text-secondary shadow-subtle mb-6 backdrop-blur-sm animate-fade-in">
          <span className="flex h-1.5 w-1.5 rounded-full bg-neutral-900 animate-pulse-subtle" />
          <span className="tracking-wide uppercase text-[11px] font-semibold text-neutral-800">
            Autonomous AI Workflows
          </span>
          <span className="text-neutral-300">|</span>
          <span className="text-text-muted text-[11px]">Beyond Simple Chat</span>
        </div>

        {/* Main Heading */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-semibold tracking-tight text-neutral-950 leading-[1.08] sm:leading-[1.06]">
          Give AI a goal.<br />
          <span className="text-neutral-500 font-normal">Let it do the work.</span>
        </h1>

        {/* Supporting Line */}
        <p className="mx-auto mt-6 max-w-2xl text-base sm:text-lg text-text-secondary font-normal leading-relaxed">
          An autonomous AI system that understands your objective, plans the multi-step workflow, executes specialized tools, and delivers verified results.
        </p>

        {/* Interactive Command Input Centerpiece */}
        <div id="command-input" className="mt-10 sm:mt-12 scroll-mt-24">
          <CommandInput onSubmit={onSubmitGoal} autoFocus={true} />
        </div>

        {/* Clickable Example Prompts */}
        <ExamplePrompts onSelectPrompt={onSubmitGoal} />

        {/* Trust & Performance Metrics Bar */}
        <div className="mt-12 flex flex-wrap items-center justify-center gap-6 text-xs text-text-muted">
          <div className="flex items-center gap-1.5">
            <ShieldCheck className="h-4 w-4 text-emerald-600" />
            <span>Deterministic multi-step verification</span>
          </div>
          <div className="hidden sm:inline text-neutral-300">•</div>
          <div className="flex items-center gap-1.5">
            <Zap className="h-4 w-4 text-neutral-700" />
            <span>Live autonomous tool orchestration</span>
          </div>
          <div className="hidden sm:inline text-neutral-300">•</div>
          <div className="flex items-center gap-1.5">
            <Sparkles className="h-4 w-4 text-neutral-700" />
            <span>Zero prompt boilerplate required</span>
          </div>
        </div>

      </div>

    </section>
  );
}
