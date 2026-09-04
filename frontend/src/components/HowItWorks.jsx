import React from 'react';

export default function HowItWorks() {
  const steps = [
    {
      number: '01',
      title: 'Give it a goal',
      description: 'Describe what you want the autonomous agent to accomplish.'
    },
    {
      number: '02',
      title: 'AI plans',
      description: 'The system breaks the goal into smaller executable steps.'
    },
    {
      number: '03',
      title: 'AI executes',
      description: 'The agent carries out the workflow using available tools.'
    },
    {
      number: '04',
      title: 'Verify & deliver',
      description: 'The system checks the result and presents the final output.'
    }
  ];

  return (
    <section id="how-it-works" className="info-section">
      <div className="section-heading">
        <span>HOW IT WORKS</span>
        <h2>From goal to completion</h2>
        <p>
          Your goal becomes an executable workflow instead of a simple
          conversation.
        </p>
      </div>

      <div className="steps-grid">
        {steps.map((step) => (
          <div className="info-card" key={step.number}>
            <div className="step-number">{step.number}</div>
            <h3>{step.title}</h3>
            <p>{step.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}