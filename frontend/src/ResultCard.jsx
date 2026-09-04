import React from 'react';

export default function ResultCard({ result, onViewResult }) {
  if (!result) return null;

  return (
    <div className="mt-4 rounded-xl border border-slate-200 bg-white p-4">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-slate-900">
            Workflow complete
          </p>

          <p className="mt-1 text-sm text-slate-500">
            Your result is ready to inspect.
          </p>
        </div>

        <button
          type="button"
          onClick={() => onViewResult?.(result)}
          className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800"
        >
          View result
        </button>
      </div>
    </div>
  );
}