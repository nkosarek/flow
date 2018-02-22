import React, { Component } from 'react';
import Space from './Space';

export default class Board extends Component {

  static createSpacesState(rows, cols, dots) {
    const spaces = new Array(rows);
    for( let row = 0; row < rows; row++ ) {
      spaces[row] = new Array(cols);
      for( let col = 0; col < cols; col++ ) {
        spaces[row][col] = {
          loc: {row, col},
          dot: null,
          pipe: null,
        };
      }
    }
    for( let dotIndex = 0; dotIndex < dots.length; dotIndex++ ) {
      let [ dotRow0, dotCol0, dotRow1, dotCol1 ] = dots[dotIndex];
      spaces[dotRow0][dotCol0].dot = {color: dotIndex, other: {row: dotRow1, col: dotCol1}}
      spaces[dotRow1][dotCol1].dot = {color: dotIndex, other: {row: dotRow0, col: dotCol0}}
    }
    return spaces;
  }

  static getSpace = (spaces, row, col) => {
    return spaces[row][col];
  }

  static areAdjacentSpaces(row0, col0, row1, col1) {
    const rowDiff = row0 - row1;
    const colDiff = col0 - col1;
    if( (rowDiff === 0 && (colDiff === 1 || colDiff === -1)) ||
        (colDiff === 0 && (rowDiff === 1 || rowDiff === -1)) ) {
      return true;
    } else {
      return false;
    }
  }

  static clearPipe(spaces, spaceLoc) {
    if( spaceLoc === null ) {
      return;
    }
    let space = Board.getSpace(spaces, spaceLoc.row, spaceLoc.col);

    // Clear next pointer in last space in pipe
    if( space.pipe !== null && space.pipe.last !== null ) {
      let { row: lastRow, col: lastCol } = space.pipe.last;
      let lastPipeSpace = Board.getSpace(spaces, lastRow, lastCol);
      //assert( lastPipeSpace.pipe !== null );
      lastPipeSpace.pipe.next = null;
    } else if( space.pipe === null ) {
      return;
    }

    // While there is a next pipe space to clear, clear its pipe
    while( spaceLoc !== null ) {
      space = Board.getSpace(spaces, spaceLoc.row, spaceLoc.col);
      spaceLoc = space.pipe.next;
      space.pipe = null;
    }
  }

  static checkLevelComplete(spaces) {
    const rows = spaces.length;
    const cols = spaces[0].length;
    for( let row = 0; row < rows; row++ ) {
      for( let col = 0; col < cols; col++ ) {
        let space = Board.getSpace(spaces, row, col);
        if( space.pipe === null ) {
          return false;
        }
      }
    }
    return true;
  }

  static clearBoard(spaces) {
    const rows = spaces.length;
    const cols = spaces[0].length;
    for( let row = 0; row < rows; row++ ) {
      for( let col = 0; col < cols; col++ ) {
        let space = Board.getSpace(spaces, row, col);
        space.pipe = null;
      }
    }
  }

  render() {
    const {
      spaces = [[null]],
      onMouseDown,
      onMouseEnter,
    } = this.props;

    const rows = spaces.length;
    const cols = spaces[0].length;

    const rowRange = Array.from(new Array(rows).keys());
    const colRange = Array.from(new Array(cols).keys());

    const boardRows = rowRange.map(row =>
      <div
        key={row}
        className='board-row'
      >
        {
          colRange.map(col =>
            <Space
              key={(row * cols) + col}
              row={row}
              col={col}
              dot={Board.getSpace(spaces, row, col).dot}
              pipe={Board.getSpace(spaces, row, col).pipe}
              onMouseDown={onMouseDown}
              onMouseEnter={onMouseEnter}
            />
          )
        }
      </div>
    );

    return (
      <div 
        className='game-board'
      >
        {boardRows}
      </div>
    );
  }
}
