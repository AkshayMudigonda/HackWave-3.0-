import React from 'react';

export default function Footer({ onOpenArchitecture }) {
  return (
    <footer className="footer">
      <div>
        <strong>Autonomous AI Workflows</strong>
        <p>Turn goals into autonomous workflows.</p>
      </div>

      <button onClick={onOpenArchitecture}>
        View Architecture
      </button>
    </footer>
  );
}