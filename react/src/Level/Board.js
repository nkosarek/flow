import React, { Component } from 'react';
import Space from './Space';

// TODO: updateStateOnMouseLeave (leave board)

const updateStateOnMouseDown = (row, col) => (prevState) => {
  const { spaces, pipeEndLoc } = prevState;
  const space = Board.getSpace(spaces, row, col);
  let newPipeEndLoc = pipeEndLoc;

  // TODO: buildingPipe for onMouseLeave
  if( space.dot !== null ) {
    const color = space.dot.color;
    if( space.pipe === null || space.pipe.next === null ) {
      Board.clearPipe(spaces, space.dot.other);
    } else {
      Board.clearPipe(spaces, space.pipe.next);
    }
    space.pipe = {color, last: null, next: null};
    newPipeEndLoc = {row, col};
    //Board.checkNewMove(spaces, space)
  } else if( space.pipe !== null ) {
    Board.clearPipe(spaces, space.pipe.next)
    newPipeEndLoc = {row, col};
    //Board.checkNewMove(spaces, space)
  }

  return {
    spaces,
    pipeEndLoc: newPipeEndLoc,
    isMouseDown: true,
    levelComplete: false,
  };
}

const updateStateOnMouseEnter = (row, col) => (prevState) => {
  const { spaces, isMouseDown, pipeEndLoc } = prevState;
  if( !isMouseDown || pipeEndLoc === null ) {
    return prevState;
  }
  const dstSpace = Board.getSpace(spaces, row, col);
  const pipeEndSpace = Board.getSpace(spaces, pipeEndLoc.row, pipeEndLoc.col);

  if( pipeEndSpace.pipe === null ) {
    alert("WTF MAN");
  }

  let newPipeEndLoc = pipeEndLoc;

  // Mouse has returned to a space in the currently advancing pipe
  if( dstSpace.pipe !== null && dstSpace.pipe.color === pipeEndSpace.pipe.color ) {
    // assert( pipeEndSpace.pipe !== null );
    if( dstSpace.pipe.next !== null ) {
      Board.clearPipe(spaces, dstSpace.pipe.next)
    }
    newPipeEndLoc = {row, col};

  // Mouse has gone past the second dot space after completing the pipe
  } else if( (pipeEndSpace.dot !== null) &&
            !(pipeEndSpace.pipe !== null && pipeEndSpace.pipe.last === null) ) {
    // DO NOTHING

  // Mouse has moved to a space adjacent to the current end of the pipe
  } else if( Board.areAdjacentSpaces(row, col, pipeEndLoc.row, pipeEndLoc.col) ) {
    if( dstSpace.dot === null ) {
      Board.clearPipe(spaces, dstSpace.loc);
      pipeEndSpace.pipe.next = dstSpace.loc;
      dstSpace.pipe = {
        color: pipeEndSpace.pipe.color,
        // TODO: Would assigning directly to pipeEndLoc cause aliasing issue?
        last: pipeEndLoc,
        next: null,
      }
      newPipeEndLoc = {row, col};

    } else if( dstSpace.dot.color === pipeEndSpace.pipe.color ) {
      pipeEndSpace.pipe.next = dstSpace.loc;
      dstSpace.pipe = {
        color: pipeEndSpace.pipe.color,
        last: pipeEndLoc,
        next: null,
      }
      newPipeEndLoc = {row, col};
    }
  }

  return {
    spaces,
    pipeEndLoc: newPipeEndLoc,
  };
}

const updateStateOnMouseUp = () => (prevState) => {
  const { spaces, pipeEndLoc } = prevState;
  if( pipeEndLoc !== null ) {
    const pipeEndSpace = Board.getSpace(spaces, pipeEndLoc.row, pipeEndLoc.col);
    if( pipeEndSpace.pipe.next === null && pipeEndSpace.pipe.last === null ) {
      Board.clearPipe(spaces, pipeEndLoc);
    }
  }
  const levelComplete = Board.checkLevelComplete(spaces);
  return {
    spaces,
    isMouseDown: false,
    pipeEndLoc: null,
    levelComplete,
  }
}

export default class Board extends Component {

  /*** STATIC METHODS ***/

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
        let space = spaces[row][col];
        if( space.pipe === null ) {
          return false;
        }
      }
    }
    return true;
  }

  /*** NON-RENDER LIFECYCLE METHODS ***/

  constructor(props) {
    super(props);

    const {
      rows,
      cols,
      dots,
    } = this.props;

    this.state = {
      spaces: Board.createSpacesState(rows, cols, dots),
      isMouseDown: false,
      pipeEndLoc: null,
      levelComplete: false,
    };

    this.getSpaceDot = this.getSpaceDot.bind(this);
    this.getSpacePipe = this.getSpacePipe.bind(this);

    this.onMouseDown = this.onMouseDown.bind(this);
    this.onMouseEnter = this.onMouseEnter.bind(this);
    this.onMouseUp = this.onMouseUp.bind(this);
  }

  componentDidMount() {
    window.addEventListener('mouseup', this.onMouseUp);
  }

  /*** EVENT HANDLERS ***/

  onMouseDown(row, col) {
    this.setState(updateStateOnMouseDown(row, col));
  }
  
  onMouseEnter(event, row, col) {
    this.setState(updateStateOnMouseEnter(row, col));
  }

  onMouseUp() {
    this.setState(updateStateOnMouseUp());
  }

  /*** GETTERS FOR RENDER ***/

  getSpaceDot(row, col) {
    const { spaces } = this.state;
    const space = Board.getSpace(spaces, row, col);
    return space.dot;
  }

  getSpacePipe(row, col) {
    const { spaces } = this.state;
    const space = Board.getSpace(spaces, row, col);
    return space.pipe;
  }

  /*** RENDER ***/

  render() {
    const {
      rows = 1,
      cols = 1,
    } = this.props;

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
              dot={this.getSpaceDot(row, col)}
              pipe={this.getSpacePipe(row, col)}
              onMouseDown={this.onMouseDown}
              onMouseEnter={this.onMouseEnter}
            />
          )
        }
      </div>
    );

    return (
      <div 
        className='game-board'
        onMouseUp={this.onMouseUp}
      >
        <div>
          {boardRows}
        </div>
        {this.state.levelComplete
          ? <p>AHHHHHH</p>
          : null
        }
      </div>
    );
  }
}
