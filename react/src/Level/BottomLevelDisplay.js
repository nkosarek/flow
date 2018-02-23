import React from 'react';
import { Link } from 'react-router-dom';

export default function TopLevelDisplay({
  lastLevelPath,
  onResetLevel,
  nextLevelPath
}) {
  return (
    <div>
      <span>
        <Link to={lastLevelPath}>
          <button>
            &lt;
          </button>
        </Link>
      </span>
      <span>
        <button
          onClick={onResetLevel}
        >
          RESET
        </button>
      </span>
      <span>
        <Link to={nextLevelPath}>
          <button>
            &gt;
          </button>
        </Link>
      </span>
    </div>
  );
}