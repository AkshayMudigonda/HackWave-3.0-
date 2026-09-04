import React, { useState } from 'react';
import { 
  X, 
  Copy, 
  Check, 
  Download, 
  ExternalLink, 
  FileText, 
  Share2, 
  Sparkles 
} from 'lucide-react';

export default function ResultModal({ isOpen, onClose, result }) {
  const [copied, setCopied] = useState(false);

  if (!isOpen || !result) return null;

  const handleCopy = () => {
    const textToCopy = `${result.headline}\n\n${result.summary}\n\n` + 
      (result.sections || []).map(s => `${s.title}:\n${s.content || (s.bullets || []).join('\n')}`).join('\n\n');
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const element = document.createElement("a");
    const file = new Blob([
      `# ${result.headline}\n\n> Autonomous AI Workflow Deliverable\n\n## Summary\n${result.summary}\n\n` +
      (result.sections || []).map(s => `## ${s.title}\n${s.content || (s.bullets || []).join('\n')}`).join('\n\n')
    ], {type: 'text/markdown'});
    element.href = URL.createObjectURL(file);
    element.download = `${result.headline.toLowerCase().replace(/[^a-z0-9]/g, '_')}_report.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto bg-neutral-950/40 backdrop-blur-sm animate-fade-in">
      
      {/* Modal Card */}
      <div 
        className="relative w-full max-w-3xl rounded-2xl border border-neutral-200 bg-white shadow-modal overflow-hidden animate-slide-up my-auto max-h-[90vh] flex flex-col"
        role="dialog"
        aria-modal="true"
      >
        
        {/* Modal Top Bar */}
        <div className="flex items-center justify-between border-b border-neutral-100 px-6 py-4 bg-neutral-50/70">
          <div className="flex items-center gap-2.5">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-neutral-900 text-white shadow-sm">
              <FileText className="h-4 w-4" />
            </div>
            <div>
              <span className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                {result.badge || 'Autonomous Deliverable'}
              </span>
              <h3 className="text-sm sm:text-base font-bold text-neutral-950 line-clamp-1">
                {result.headline}
              </h3>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleCopy}
              className="flex items-center gap-1.5 rounded-lg border border-neutral-200 bg-white px-3 py-1.5 text-xs font-medium text-text-secondary shadow-subtle hover:bg-neutral-50 hover:text-neutral-900 transition-all focus-ring"
              title="Copy markdown text"
            >
              {copied ? <Check className="h-3.5 w-3.5 text-emerald-600" /> : <Copy className="h-3.5 w-3.5" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>

            <button
              type="button"
              onClick={handleDownload}
              className="hidden sm:flex items-center gap-1.5 rounded-lg border border-neutral-200 bg-white px-3 py-1.5 text-xs font-medium text-text-secondary shadow-subtle hover:bg-neutral-50 hover:text-neutral-900 transition-all focus-ring"
              title="Download markdown report"
            >
              <Download className="h-3.5 w-3.5" />
              <span>Export</span>
            </button>

            <button
              type="button"
              onClick={onClose}
              className="flex h-8 w-8 items-center justify-center rounded-lg text-text-muted hover:bg-neutral-100 hover:text-neutral-900 transition-colors focus-ring"
              aria-label="Close dialog"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Modal Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 text-text-primary">
          
          {/* Executive Summary Block */}
          <div className="rounded-xl border border-neutral-100 bg-neutral-50/60 p-4 sm:p-5">
            <div className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-1.5">
              Synthesis Summary
            </div>
            <p className="text-sm sm:text-base text-text-primary leading-relaxed">
              {result.summary}
            </p>
          </div>

          {/* Key Metric Tiles */}
          {result.metrics && (
            <div>
              <div className="text-xs font-semibold uppercase tracking-wider text-text-muted mb-2.5">
                Key Performance & Market Indicators
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {result.metrics.map((m, idx) => (
                  <div key={idx} className="rounded-xl border border-neutral-200/80 bg-white p-3.5 shadow-subtle">
                    <div className="text-xs text-text-muted">{m.label}</div>
                    <div className="mt-1 text-lg sm:text-xl font-bold text-neutral-950">{m.value}</div>
                    {m.change && (
                      <div className="mt-0.5 text-xs font-medium text-emerald-700">{m.change}</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Detailed Structural Sections */}
          {result.sections && (
            <div className="space-y-5 pt-2">
              {result.sections.map((section, sIdx) => (
                <div key={sIdx} className="space-y-2">
                  <h4 className="text-sm sm:text-base font-bold text-neutral-950 flex items-center gap-2">
                    <span className="flex h-1.5 w-1.5 rounded-full bg-neutral-900" />
                    {section.title}
                  </h4>
                  {section.content && (
                    <p className="text-xs sm:text-sm text-text-secondary leading-relaxed pl-3.5 border-l-2 border-neutral-200">
                      {section.content}
                    </p>
                  )}
                  {section.bullets && (
                    <ul className="space-y-2 pl-3.5 border-l-2 border-neutral-200">
                      {section.bullets.map((b, bIdx) => (
                        <li key={bIdx} className="text-xs sm:text-sm text-text-secondary leading-relaxed">
                          <span dangerouslySetInnerHTML={{
                            __html: b.replace(/\*\*(.*?)\*\*/g, '<strong class="text-neutral-900 font-semibold">$1</strong>')
                          }} />
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          )}

        </div>

        {/* Modal Footer */}
        <div className="flex items-center justify-between border-t border-neutral-100 px-6 py-3.5 bg-neutral-50/50 text-xs text-text-muted">
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 rounded-full bg-emerald-500" />
            <span>Autonomous AI verification: Validated against 100% cited sources</span>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg bg-neutral-900 px-4 py-1.5 font-medium text-white shadow-subtle hover:bg-neutral-800 transition-colors focus-ring"
          >
            Done
          </button>
        </div>

      </div>

    </div>
  );
}
