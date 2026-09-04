import React from 'react';

export default function ExamplePrompts({ onSelect }) {
  const prompts = [
    'Research the best laptops under ₹50,000',
    'Compare the top smartphones under ₹30,000',
    'Find the best productivity tools for a student',
    'Create a travel plan for a 3-day trip'
  ];

  return (
    <div className="mt-6">
      <p className="text-sm text-slate-500 mb-3">
        Try an example
      </p>

      <div className="flex flex-wrap gap-2">
        {prompts.map((prompt) => (
          <button
            key={prompt}
            type="button"
            onClick={() => onSelect?.(prompt)}
            className="px-3 py-2 rounded-lg border border-slate-200 bg-white text-sm text-slate-700 hover:border-slate-400 hover:bg-slate-50 transition"
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
}