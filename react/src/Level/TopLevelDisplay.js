import React from 'react';
import { Link } from 'react-router-dom';

export default function TopLevelDisplay({
  numMoves,
  levelSelectPath,
}) {
  return (
    <div>
      <span>
        <Link to={levelSelectPath}>
          <button>
            &lt;-Back
          </button>
        </Link>
      </span>
      <span>
        Moves: {numMoves}
      </span>
    </div>
  );
}