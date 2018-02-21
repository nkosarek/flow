import React from 'react';

export default function TopLevelDisplay({
  numMoves,
  onBackToLevelSelect,
}) {
  return (
    <div>
      <span>
        <button
          onClick={onBackToLevelSelect}
        >
          &lt;-Back
        </button>
      </span>
      <span>
        Moves: {numMoves}
      </span>
    </div>
  );
}