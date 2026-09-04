import React, { useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import WorkflowCard from './WorkflowCard';
import CommandInput from './CommandInput';
import { Sparkles, MessageSquare, ArrowDown, RotateCcw } from 'lucide-react';

export default function Workspace({
  turns,
  isExecuting,
  onSendMessage,
  onViewResult,
  onFastForward,
  onReset
}) {
  const bottomRef = useRef(null);

  // Auto scroll gently to bottom on update
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [turns]);

  return (
    <div className="flex min-h-[calc(100vh-4rem)] flex-col justify-between">
      
      {/* Workspace Stream */}
      <main className="flex-1 w-full max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        {/* Workspace Context Bar */}
        <div className="flex items-center justify-between border-b border-border-subtle pb-3 text-xs text-text-muted">
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 rounded-full bg-emerald-500" />
            <span className="font-medium text-neutral-800">Autonomous Session Active</span>
          </div>
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={onReset}
              className="flex items-center gap-1 hover:text-neutral-900 transition-colors focus-ring rounded"
            >
              <RotateCcw className="h-3 w-3" />
              <span>Reset session</span>
            </button>
          </div>
        </div>

        {/* Conversation Turns */}
        {turns.map((turn, tIdx) => (
          <div key={tIdx} className="space-y-6">
            
            {/* User Message */}
            {turn.userMessage && (
              <ChatMessage message={turn.userMessage} />
            )}

            {/* AI Acknowledgment */}
            {turn.aiMessage && (
              <ChatMessage message={turn.aiMessage} />
            )}

            {/* Workflow Execution Card */}
            {turn.workflow && (
              <div className="py-2">
                <WorkflowCard
                  workflow={turn.workflow}
                  currentStepIndex={turn.currentStepIndex}
                  isCompleted={turn.isCompleted}
                  elapsedSeconds={turn.elapsedSeconds}
                  onViewResult={() => onViewResult(turn.workflow.result)}
                  onFastForward={onFastForward}
                />
              </div>
            )}

          </div>
        ))}

        <div ref={bottomRef} className="h-4" />
      </main>

      {/* Floating Bottom Input Area */}
      <footer className="sticky bottom-0 z-30 w-full border-t border-border-subtle bg-white/95 backdrop-blur-md px-4 py-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          
          {/* Quick Follow-up Suggestions */}
          <div className="mb-2.5 flex flex-wrap items-center gap-1.5 text-xs">
            <span className="text-text-subtle text-[11px] font-medium mr-1 hidden sm:inline">
              Suggested next actions:
            </span>
            {[
              "Deep dive into battery supply chains",
              "Draft executive email for leadership",
              "Benchmark against European targets"
            ].map((suggest, sIdx) => (
              <button
                key={sIdx}
                type="button"
                disabled={isExecuting}
                onClick={() => onSendMessage(suggest)}
                className="rounded-full border border-neutral-200 bg-neutral-50 px-2.5 py-1 text-[11px] text-text-secondary hover:bg-neutral-100 hover:text-neutral-900 transition-colors disabled:opacity-50"
              >
                + {suggest}
              </button>
            ))}
          </div>

          <CommandInput
            onSubmit={onSendMessage}
            isExecuting={isExecuting}
            placeholder="Continue the conversation or give a follow-up goal..."
            compact={true}
          />
          
          <div className="mt-2 text-center text-[11px] text-text-subtle">
            Autonomous AI autonomously plans, coordinates tools, and executes multi-turn tasks.
          </div>
        </div>
      </footer>

    </div>
  );
}
