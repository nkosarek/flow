import React from 'react';

export default function Space({
  row,
  col,
  dot,
  pipe,
  onMouseDown,
  onMouseEnter,
}) {
  let text = (dot === null) ? '-' : dot.color.toString();
  if( pipe === null ) {
    text += '-';
  } else {
    text += pipe.color;
  }

  return (
    <span
      className="game-space"
      onMouseDown={() => onMouseDown(row, col)}
      onMouseEnter={() => onMouseEnter(row, col)}
    >
      <button>
        {text}
      </button>
    </span>
  );
}
