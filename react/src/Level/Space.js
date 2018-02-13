import React from 'react';

export default function Space({
row,
col,
dot,
pipe,
onMouseDown,
onMouseEnter,
}) {
  let text = (dot === null) ? 'Ay' : 'A' + dot;
  if( pipe === null ) {
    text += 'y';
  } else {
    text += pipe;
  }

  return (
    <span
      className="game-space"
      onMouseDown={() => onMouseDown(row, col)}
      onMouseEnter={(e) => onMouseEnter(e, row, col)}
    >
      <button>
        {text}
      </button>
    </span>
  );
}
