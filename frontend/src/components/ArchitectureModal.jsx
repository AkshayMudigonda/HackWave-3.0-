import React from 'react';

export default function ArchitectureModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="architecture-modal"
        onClick={(e) => e.stopPropagation()}
      >
        <button className="modal-close" onClick={onClose}>
          ×
        </button>

        <span>ARCHITECTURE</span>
        <h2>How the system works</h2>

        <div className="architecture-flow">
          <div>USER GOAL</div>
          <div>↓</div>
          <div>AI PLANNER</div>
          <div>↓</div>
          <div>WORKFLOW ENGINE</div>
          <div>↓</div>
          <div>TOOLS / BROWSER / APIs</div>
          <div>↓</div>
          <div>VERIFICATION</div>
          <div>↓</div>
          <div>FINAL RESULT</div>
        </div>
      </div>
    </div>
  );
}