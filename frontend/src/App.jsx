import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './Hero';
import HowItWorks from './components/HowItWorks';
import Capabilities from './components/Capabilities';
import Footer from './components/Footer';
import Workspace from './Workspace';
import ResultModal from './ResultModal';
import ArchitectureModal from './components/ArchitectureModal';
import { submitGoal } from './api';

const createPendingWorkflow = (prompt) => ({
  title: prompt,
  category: 'Live backend request',
  steps: [
    { id: 'request', name: 'Submit goal', desc: 'Your goal was sent to the assistant API.', tool: 'HTTP POST /api/assist', logs: ['Request submitted to the configured backend.'] },
    { id: 'response', name: 'Process assistant response', desc: 'Waiting for the backend to complete the request.', tool: 'Assistant Agent', logs: [] },
  ],
});

const createResult = (prompt, response) => ({
  headline: `Assistant response: ${prompt.slice(0, 72)}${prompt.length > 72 ? '…' : ''}`,
  badge: 'Live Backend Result',
  summary: response,
  sections: [{ title: 'Assistant response', content: response }],
});

export default function App() {
  // Navigation & View Mode: 'landing' | 'workspace'
  const [viewMode, setViewMode] = useState('landing');
  
  // Execution Speed: 'normal' (1.2s/step) | 'fast' (0.5s/step) | 'instant' (0.05s)
  const [speed, setSpeed] = useState('normal');

  // Modals state
  const [selectedResult, setSelectedResult] = useState(null);
  const [isArchitectureOpen, setIsArchitectureOpen] = useState(false);

  // Workspace turns state: Array of { id, userMessage, aiMessage, workflow, currentStepIndex, isCompleted, elapsedSeconds }
  const [turns, setTurns] = useState([]);
  const [isExecuting, setIsExecuting] = useState(false);

  // Scroll smoothly to anchored sections on landing page
  const handleNavigateSection = (sectionId) => {
    if (viewMode !== 'landing') {
      setViewMode('landing');
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        el?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      const el = document.getElementById(sectionId);
      el?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Reset everything back to the clean landing state
  const handleReset = () => {
    setIsExecuting(false);
    setTurns([]);
    setViewMode('landing');
    setSelectedResult(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Main goal submission handler
  const handleStartGoal = async (promptText, options = {}) => {
    if (!promptText.trim()) return;

    // Transition to workspace mode immediately
    setViewMode('workspace');
    setIsExecuting(true);

    const workflowData = createPendingWorkflow(promptText);
    const startedAt = Date.now();

    // Initial AI greeting
    const newTurn = {
      id: 'turn-' + Date.now(),
      userMessage: {
        id: 'msg-u-' + Date.now(),
        sender: 'user',
        text: promptText,
        attachment: options.attachment
      },
      aiMessage: {
        id: 'msg-ai-' + Date.now(),
        sender: 'ai',
        text: 'Your request is being processed by the connected backend.',
        timestamp: 'Just now'
      },
      workflow: workflowData,
      currentStepIndex: 0,
      isCompleted: false,
      elapsedSeconds: 0
    };

    setTurns(prev => [...prev, newTurn]);

    try {
      const payload = await submitGoal(promptText);
      const elapsedSeconds = (Date.now() - startedAt) / 1000;
      setTurns(prevTurns => prevTurns.map(turn => turn.id === newTurn.id ? {
        ...turn,
        aiMessage: { ...turn.aiMessage, text: payload.message },
        workflow: {
          ...turn.workflow,
          steps: turn.workflow.steps.map((step, index) => index === 1 ? {
            ...step,
            desc: 'The backend returned a response for this goal.',
            logs: ['Backend response received successfully.'],
          } : step),
          result: createResult(promptText, payload.message),
        },
        currentStepIndex: 1,
        isCompleted: true,
        elapsedSeconds,
      } : turn));
    } catch (error) {
      setTurns(prevTurns => prevTurns.map(turn => turn.id === newTurn.id ? {
        ...turn,
        aiMessage: { ...turn.aiMessage, text: `Unable to complete this request: ${error.message}` },
        workflow: null,
        elapsedSeconds: (Date.now() - startedAt) / 1000,
      } : turn));
    } finally {
      setIsExecuting(false);
    }
  };

  // Instant fast-forward for the active workflow
  const handleFastForward = () => {
    // The backend does not support cancellation or streaming progress.
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#F9FAFB] text-[#0F172A]">
      
      {/* Top Navigation */}
      <Navbar
        viewMode={viewMode}
        onReset={handleReset}
        speed={speed}
        setSpeed={setSpeed}
        onOpenArchitecture={() => setIsArchitectureOpen(true)}
        onNavigateSection={handleNavigateSection}
      />

      {/* Main Content Area: Landing View vs. Workspace View */}
      {viewMode === 'landing' ? (
        <main className="flex-1 animate-fade-in">
          <Hero onSubmitGoal={handleStartGoal} />
          <HowItWorks />
          <Capabilities />
        </main>
      ) : (
        <div className="flex-1 animate-fade-in">
          <Workspace
            turns={turns}
            isExecuting={isExecuting}
            onSendMessage={handleStartGoal}
            onViewResult={(result) => setSelectedResult(result)}
            onFastForward={handleFastForward}
            onReset={handleReset}
          />
        </div>
      )}

      {/* Footer (always visible on landing) */}
      {viewMode === 'landing' && (
        <Footer onOpenArchitecture={() => setIsArchitectureOpen(true)} />
      )}

      {/* Rich Deliverable Result Modal / Drawer */}
      <ResultModal
        isOpen={Boolean(selectedResult)}
        result={selectedResult}
        onClose={() => setSelectedResult(null)}
      />

      {/* System Architecture Specification Modal */}
      <ArchitectureModal
        isOpen={isArchitectureOpen}
        onClose={() => setIsArchitectureOpen(false)}
      />

    </div>
  );
}
