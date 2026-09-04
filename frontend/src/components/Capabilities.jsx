import React from 'react';

export default function Capabilities() {
  const capabilities = [
    {
      icon: '🎯',
      title: 'Goal-driven',
      description: 'Start with an objective instead of writing every individual instruction.'
    },
    {
      icon: '🧠',
      title: 'Multi-step reasoning',
      description: 'Break complex objectives into manageable workflow steps.'
    },
    {
      icon: '🌐',
      title: 'Tool execution',
      description: 'Designed to work with browsers, APIs and other execution environments.'
    },
    {
      icon: '✓',
      title: 'Verification',
      description: 'Check completed actions before delivering the final result.'
    }
  ];

  return (
    <section id="capabilities" className="info-section">
      <div className="section-heading">
        <span>CAPABILITIES</span>
        <h2>Built for autonomous execution</h2>
      </div>

      <div className="capabilities-grid">
        {capabilities.map((item) => (
          <div className="info-card" key={item.title}>
            <div className="capability-icon">{item.icon}</div>
            <h3>{item.title}</h3>
            <p>{item.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}