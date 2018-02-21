import React from 'react';

export default function TopLevelDisplay({
  onLastLevel,
  onResetLevel,
  onNextLevel,
}) {
  return (
    <div>
      <span>
        <button
          onClick={onLastLevel}
        >
          &lt;
        </button>
      </span>
      <span>
        <button
          onClick={onResetLevel}
        >
          RESET
        </button>
      </span>
      <span>
        <button
          onClick={onNextLevel}
        >
          &gt;
        </button>
      </span>
    </div>
  );
}