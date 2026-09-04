import React, { useState } from 'react';
import { 
  Check, 
  Loader2, 
  Circle, 
  ChevronDown, 
  ChevronUp, 
  Terminal, 
  Wrench,
  Clock
} from 'lucide-react';

export default function WorkflowStep({ 
  step, 
  status, // 'pending' | 'active' | 'completed'
  index, 
  isLast = false 
}) {
  const [showLogs, setShowLogs] = useState(false);

  const getStatusIcon = () => {
    switch (status) {
      case 'completed':
        return (
          <div className="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-600 text-white shadow-sm transition-all duration-300">
            <Check className="h-3.5 w-3.5 stroke-[3]" />
          </div>
        );
      case 'active':
        return (
          <div className="relative flex h-6 w-6 items-center justify-center rounded-full bg-neutral-900 text-white shadow-sm">
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            <span className="absolute -inset-1 rounded-full bg-neutral-900/20 animate-ping" />
          </div>
        );
      case 'pending':
      default:
        return (
          <div className="flex h-6 w-6 items-center justify-center rounded-full border border-neutral-300 bg-white text-neutral-400">
            <Circle className="h-2.5 w-2.5 fill-current text-neutral-300" />
          </div>
        );
    }
  };

  const getStatusBadge = () => {
    switch (status) {
      case 'completed':
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 border border-emerald-200/60 px-2 py-0.5 rounded-full">
            Done
          </span>
        );
      case 'active':
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-medium text-neutral-900 bg-neutral-100 border border-neutral-200 px-2 py-0.5 rounded-full">
            <span className="h-1.5 w-1.5 rounded-full bg-neutral-900 animate-pulse-subtle" />
            Executing
          </span>
        );
      case 'pending':
      default:
        return (
          <span className="text-[11px] text-text-subtle">
            Queued
          </span>
        );
    }
  };

  return (
    <div className="relative flex gap-3.5 sm:gap-4 group">
      
      {/* Vertical Connecting Line */}
      {!isLast && (
        <div 
          className={`absolute left-3 top-6 bottom-0 w-[1.5px] -ml-[0.75px] transition-colors duration-500 ${
            status === 'completed' 
              ? 'bg-emerald-500' 
              : status === 'active'
                ? 'bg-gradient-to-b from-neutral-800 to-neutral-200'
                : 'bg-neutral-200'
          }`} 
        />
      )}

      {/* Node Indicator Icon */}
      <div className="relative z-10 shrink-0 pt-0.5">
        {getStatusIcon()}
      </div>

      {/* Step Content Card */}
      <div className={`flex-1 pb-5 ${status === 'pending' ? 'opacity-60' : 'opacity-100'} transition-opacity duration-300`}>
        
        <div className="flex flex-wrap items-center justify-between gap-2">
          
          <div className="flex items-center gap-2">
            <span className={`text-xs sm:text-sm font-semibold tracking-tight ${
              status === 'active' 
                ? 'text-neutral-950 font-bold' 
                : status === 'completed'
                  ? 'text-neutral-900'
                  : 'text-neutral-600'
            }`}>
              {step.name}
            </span>

            {/* Tool Badge */}
            {step.tool && (
              <span className="hidden sm:inline-flex items-center gap-1 rounded bg-neutral-100 px-1.5 py-0.5 text-[10px] font-mono text-neutral-600 border border-neutral-200/60">
                <Wrench className="h-2.5 w-2.5" />
                {step.tool}
              </span>
            )}
          </div>

          <div className="flex items-center gap-2">
            {getStatusBadge()}
          </div>

        </div>

        {/* Step Description */}
        <p className="mt-1 text-xs sm:text-[13px] text-text-secondary leading-relaxed">
          {step.desc}
        </p>

        {/* Inspectable Execution Logs (Active or Completed) */}
        {step.logs && step.logs.length > 0 && status !== 'pending' && (
          <div className="mt-2.5">
            <button
              type="button"
              onClick={() => setShowLogs(!showLogs)}
              className="flex items-center gap-1.5 text-[11px] font-mono font-medium text-text-muted hover:text-neutral-900 transition-colors focus-ring rounded py-0.5"
            >
              <Terminal className="h-3 w-3" />
              <span>{showLogs ? 'Hide execution trace' : `Inspect trace (${step.logs.length} operations)`}</span>
              {showLogs ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
            </button>

            {showLogs && (
              <div className="mt-2 rounded-lg bg-neutral-900 p-2.5 font-mono text-[11px] text-neutral-300 shadow-inner border border-neutral-800 space-y-1 animate-fade-in overflow-x-auto">
                <div className="flex items-center justify-between pb-1 border-b border-neutral-800 text-[10px] text-neutral-500 uppercase tracking-wider">
                  <span>Tool Output Console</span>
                  <span>PID: 0x4B29</span>
                </div>
                {step.logs.map((log, lIdx) => (
                  <div key={lIdx} className="flex items-start gap-2">
                    <span className="text-neutral-600 select-none">&gt;</span>
                    <span className="text-neutral-300">{log}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

      </div>

    </div>
  );
}
