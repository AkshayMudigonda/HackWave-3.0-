import React from 'react';

export default function Navbar({
  viewMode,
  onReset,
  speed,
  setSpeed,
  onOpenArchitecture,
  onNavigateSection
}) {
  return (
    <nav className="navbar">
      <div className="navbar-brand" onClick={onReset}>
        <span>⚡</span>
        <strong>Autonomous AI</strong>
      </div>

      <div className="navbar-links">
        {viewMode === 'landing' && (
          <>
            <button onClick={() => onNavigateSection('how-it-works')}>
              How it works
            </button>

            <button onClick={() => onNavigateSection('capabilities')}>
              Capabilities
            </button>
          </>
        )}

        <button onClick={onOpenArchitecture}>
          Architecture
        </button>

        {viewMode === 'workspace' && (
          <button onClick={onReset}>
            Home
          </button>
        )}
      </div>

      {viewMode === 'workspace' && (
        <select
          value={speed}
          onChange={(e) => setSpeed(e.target.value)}
          className="speed-select"
        >
          <option value="normal">Normal</option>
          <option value="fast">Fast</option>
          <option value="instant">Instant</option>
        </select>
      )}
    </nav>
  );
}