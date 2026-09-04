import React, { useState, useRef, useEffect } from 'react';
import { 
  ArrowUp, 
  Paperclip, 
  SlidersHorizontal, 
  Sparkles, 
  FileText, 
  X, 
  Globe, 
  Terminal, 
  Database 
} from 'lucide-react';

export default function CommandInput({ 
  onSubmit, 
  isExecuting = false, 
  placeholder = "What would you like me to accomplish?",
  compact = false,
  autoFocus = false
}) {
  const [value, setValue] = useState('');
  const [attachment, setAttachment] = useState(null);
  const [showToolsMenu, setShowToolsMenu] = useState(false);
  const [selectedTools, setSelectedTools] = useState({
    webSearch: true,
    sandbox: true,
    dataAnalysis: true
  });

  const textareaRef = useRef(null);

  // Auto-resize textarea height smoothly
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`;
    }
  }, [value]);

  useEffect(() => {
    if (autoFocus && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [autoFocus]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    const trimmed = value.trim();
    if (!trimmed || isExecuting) return;
    onSubmit(trimmed, {
      attachment,
      tools: selectedTools
    });
    setValue('');
    setAttachment(null);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleMockAttach = () => {
    if (attachment) {
      setAttachment(null);
    } else {
      setAttachment({
        name: 'dataset_reference_v3.csv',
        size: '1.4 MB'
      });
    }
  };

  const toggleTool = (toolKey) => {
    setSelectedTools(prev => ({
      ...prev,
      [toolKey]: !prev[toolKey]
    }));
  };

  return (
    <div className={`w-full relative transition-all duration-300 ${compact ? 'max-w-4xl' : 'max-w-3xl mx-auto'}`}>
      
      {/* Outer Glow / Border Shell */}
      <div className={`relative rounded-2xl bg-white border border-border-subtle shadow-command transition-all duration-200 focus-within:border-neutral-400 focus-within:shadow-xl`}>
        
        {/* Attached File Preview Badge (if attached) */}
        {attachment && (
          <div className="mx-4 mt-3 flex items-center gap-2 rounded-lg bg-neutral-50 border border-neutral-200/80 px-3 py-1.5 text-xs text-neutral-800 animate-fade-in w-fit">
            <FileText className="h-3.5 w-3.5 text-neutral-600" />
            <span className="font-medium">{attachment.name}</span>
            <span className="text-text-muted">({attachment.size})</span>
            <button 
              type="button" 
              onClick={() => setAttachment(null)}
              className="ml-1 text-text-muted hover:text-neutral-900 rounded p-0.5"
              aria-label="Remove attachment"
            >
              <X className="h-3 w-3" />
            </button>
          </div>
        )}

        {/* Text Input Area */}
        <div className="px-4 pt-3.5 pb-2">
          <textarea
            ref={textareaRef}
            rows={1}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={isExecuting}
            className="w-full resize-none bg-transparent text-sm sm:text-base font-normal text-text-primary placeholder:text-text-subtle focus:outline-none disabled:opacity-60 leading-relaxed max-h-[180px]"
            style={{ minHeight: compact ? '40px' : '52px' }}
          />
        </div>

        {/* Bottom Control Bar */}
        <div className="flex items-center justify-between border-t border-neutral-100 px-3 py-2.5">
          
          {/* Left Action Buttons */}
          <div className="flex items-center gap-1.5 relative">
            
            {/* Attachment Button */}
            <button
              type="button"
              onClick={handleMockAttach}
              disabled={isExecuting}
              className={`flex items-center gap-1 rounded-lg px-2 py-1.5 text-xs font-medium transition-colors focus-ring ${
                attachment 
                  ? 'bg-neutral-100 text-neutral-900 font-semibold' 
                  : 'text-text-muted hover:bg-surface-hover hover:text-neutral-900'
              }`}
              title="Attach dataset or document"
              aria-label="Attach file"
            >
              <Paperclip className="h-4 w-4" />
              <span className="hidden sm:inline text-[12px]">Attach</span>
            </button>

            {/* Tool Selection Menu Trigger */}
            <div className="relative">
              <button
                type="button"
                onClick={() => setShowToolsMenu(!showToolsMenu)}
                disabled={isExecuting}
                className={`flex items-center gap-1 rounded-lg px-2 py-1.5 text-xs font-medium transition-colors focus-ring ${
                  showToolsMenu 
                    ? 'bg-neutral-100 text-neutral-900' 
                    : 'text-text-muted hover:bg-surface-hover hover:text-neutral-900'
                }`}
                title="Configure Autonomous Tools"
                aria-label="Configure tools"
              >
                <SlidersHorizontal className="h-3.5 w-3.5" />
                <span className="hidden sm:inline text-[12px]">Autonomous Tools</span>
              </button>

              {/* Tools Popover */}
              {showToolsMenu && (
                <div className="absolute left-0 bottom-full mb-2 w-64 rounded-xl border border-border-subtle bg-white p-2.5 shadow-modal z-30 animate-slide-up text-xs">
                  <div className="mb-2 px-1 text-[11px] font-semibold uppercase tracking-wider text-text-muted">
                    Execution Capabilities
                  </div>
                  <div className="space-y-1">
                    <button
                      type="button"
                      onClick={() => toggleTool('webSearch')}
                      className="flex w-full items-center justify-between rounded-lg p-1.5 hover:bg-neutral-50 transition-colors"
                    >
                      <div className="flex items-center gap-2 text-text-secondary">
                        <Globe className="h-3.5 w-3.5 text-blue-600" />
                        <span>Web Live Retrieval</span>
                      </div>
                      <span className={`h-2 w-2 rounded-full ${selectedTools.webSearch ? 'bg-emerald-500' : 'bg-neutral-300'}`} />
                    </button>

                    <button
                      type="button"
                      onClick={() => toggleTool('sandbox')}
                      className="flex w-full items-center justify-between rounded-lg p-1.5 hover:bg-neutral-50 transition-colors"
                    >
                      <div className="flex items-center gap-2 text-text-secondary">
                        <Terminal className="h-3.5 w-3.5 text-purple-600" />
                        <span>Code & Logic Sandbox</span>
                      </div>
                      <span className={`h-2 w-2 rounded-full ${selectedTools.sandbox ? 'bg-emerald-500' : 'bg-neutral-300'}`} />
                    </button>

                    <button
                      type="button"
                      onClick={() => toggleTool('dataAnalysis')}
                      className="flex w-full items-center justify-between rounded-lg p-1.5 hover:bg-neutral-50 transition-colors"
                    >
                      <div className="flex items-center gap-2 text-text-secondary">
                        <Database className="h-3.5 w-3.5 text-amber-600" />
                        <span>Data Synthesizer</span>
                      </div>
                      <span className={`h-2 w-2 rounded-full ${selectedTools.dataAnalysis ? 'bg-emerald-500' : 'bg-neutral-300'}`} />
                    </button>
                  </div>
                  <div className="mt-2 border-t border-neutral-100 pt-1.5 px-1 text-[10px] text-text-subtle">
                    Autonomous AI will orchestrate tools based on the objective.
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right Action: Keyboard Shortcut & Send Button */}
          <div className="flex items-center gap-2">
            <span className="hidden sm:inline-block text-[11px] font-medium text-text-subtle select-none">
              Enter ↵
            </span>

            <button
              type="button"
              onClick={handleSubmit}
              disabled={!value.trim() || isExecuting}
              className={`flex h-8 w-8 items-center justify-center rounded-xl transition-all duration-200 focus-ring ${
                value.trim() && !isExecuting
                  ? 'bg-neutral-900 text-white shadow-subtle hover:bg-neutral-800 active:scale-95'
                  : 'bg-neutral-100 text-neutral-400 cursor-not-allowed'
              }`}
              aria-label="Send goal to autonomous AI"
            >
              <ArrowUp className="h-4 w-4 stroke-[2.5]" />
            </button>
          </div>

        </div>

      </div>

    </div>
  );
}
