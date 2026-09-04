import React, { useState, useEffect } from 'react';
import WorkflowStep from './WorkflowStep';
import ResultCard from './ResultCard';
import { 
  CheckCircle2, 
  Clock, 
  Layers, 
  Sparkles, 
  Play, 
  FastForward 
} from 'lucide-react';

export default function WorkflowCard({ 
  workflow, 
  currentStepIndex, 
  isCompleted, 
  elapsedSeconds, 
  onViewResult,
  onFastForward
}) {
  if (!workflow) return null;

  const totalSteps = workflow.steps.length;
  const progressPercent = isCompleted 
    ? 100 
    : Math.round(((currentStepIndex) / totalSteps) * 100);

  return (
    <div className="w-full max-w-2xl mx-auto rounded-2xl border border-border-subtle bg-white p-5 sm:p-6 shadow-elevated transition-all duration-300 animate-fade-in">
      
      {/* Workflow Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-neutral-100">
        
        <div className="flex items-center gap-2.5">
          <div className={`flex h-7 w-7 items-center justify-center rounded-lg transition-colors ${
            isCompleted 
              ? 'bg-emerald-600 text-white' 
              : 'bg-neutral-900 text-white'
          }`}>
            <Layers className="h-4 w-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-neutral-900">
                Autonomous Workflow
              </span>
              <span className="text-[11px] text-text-muted hidden sm:inline">•</span>
              <span className="text-[11px] font-medium text-text-muted hidden sm:inline">
                {workflow.category || 'Multi-step Pipeline'}
              </span>
            </div>
            <p className="text-xs text-text-subtle line-clamp-1">
              {workflow.title}
            </p>
          </div>
        </div>

        {/* Status Pill & Progress Counter */}
        <div className="flex items-center gap-2.5">
          {/* Active / Completed Pill */}
          {isCompleted ? (
            <div className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 border border-emerald-200/80 px-2.5 py-1 text-xs font-medium text-emerald-700 animate-fade-in">
              <CheckCircle2 className="h-3.5 w-3.5" />
              <span>Workflow completed</span>
            </div>
          ) : (
            <div className="inline-flex items-center gap-1.5 rounded-full bg-neutral-100 border border-neutral-200 px-2.5 py-1 text-xs font-medium text-neutral-900">
              <span className="h-2 w-2 rounded-full bg-neutral-900 animate-pulse-subtle" />
              <span>Executing</span>
            </div>
          )}

          {/* Elapsed Timer */}
          <div className="flex items-center gap-1 text-xs font-mono text-text-muted bg-neutral-50 px-2 py-0.5 rounded border border-neutral-100">
            <Clock className="h-3 w-3" />
            <span>{elapsedSeconds.toFixed(1)}s</span>
          </div>
        </div>

      </div>

      {/* Progress Bar & Counter */}
      <div className="mt-4 mb-6">
        <div className="flex items-center justify-between text-xs text-text-muted mb-1.5">
          <span className="font-medium">
            {isCompleted 
              ? `All ${totalSteps} steps completed` 
              : `${currentStepIndex + 1} / ${totalSteps} steps in progress`}
          </span>
          <span className="font-mono font-medium">{progressPercent}%</span>
        </div>
        <div className="h-1.5 w-full overflow-hidden rounded-full bg-neutral-100">
          <div 
            className={`h-full transition-all duration-500 rounded-full ${
              isCompleted ? 'bg-emerald-600' : 'bg-neutral-900'
            }`}
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Vertical Steps List */}
      <div className="space-y-0.5 pt-1">
        {workflow.steps.map((step, idx) => {
          let status = 'pending';
          if (isCompleted || idx < currentStepIndex) {
            status = 'completed';
          } else if (idx === currentStepIndex) {
            status = 'active';
          }

          return (
            <WorkflowStep
              key={step.id || idx}
              step={step}
              status={status}
              index={idx}
              isLast={idx === workflow.steps.length - 1}
            />
          );
        })}
      </div>

      {/* Fast Forward button if currently executing */}
      {!isCompleted && onFastForward && (
        <div className="mt-2 flex justify-end">
          <button
            type="button"
            onClick={onFastForward}
            className="flex items-center gap-1 text-[11px] font-medium text-text-muted hover:text-neutral-900 transition-colors focus-ring rounded py-1 px-2 hover:bg-neutral-50"
            title="Fast forward simulation to completion"
          >
            <FastForward className="h-3 w-3" />
            <span>Fast-forward execution</span>
          </button>
        </div>
      )}

      {/* Compact Result Section (Revealed when completed) */}
      {isCompleted && (
        <ResultCard 
          result={workflow.result} 
          onViewResult={onViewResult} 
        />
      )}

    </div>
  );
}
