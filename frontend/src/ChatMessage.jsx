import React from 'react';

export default function ChatMessage({ message }) {
  if (!message) return null;

  const isUser = message.sender === 'user';

  return (
    <div
      className={`flex w-full mb-4 ${
        isUser ? 'justify-end' : 'justify-start'
      }`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-black text-white'
            : 'bg-white text-slate-900 border border-slate-200'
        }`}
      >
        <div className="text-sm whitespace-pre-wrap">
          {message.text}
        </div>

        {message.timestamp && (
          <div
            className={`text-xs mt-1 ${
              isUser ? 'text-slate-300' : 'text-slate-400'
            }`}
          >
            {message.timestamp}
          </div>
        )}
      </div>
    </div>
  );
}