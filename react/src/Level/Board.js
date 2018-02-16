import React, { Component } from 'react';
import Space from './Space';

const updateStateOnMouseDown = (row, col) => (prevState) => {
  const { spaces } = prevState;
  const space = Board.getSpace(spaces, row, col);
  const currPipeEnd = {row: row, col: col}

  if( space.dot !== null ) {
    const color = space.dot.color;
    if( space.pipe === null /* TODO: || space.is_pipe_end() */) {
      //Board.clear_pipe(spaces, space.dot.other);
    } else {
      //Board.clear_pipe(spaces/* TODO: , space.next */)
    }
    space.pipe = {color: color};
    // TODO: Board.check_new_move(spaces, space)
  } else if( space.pipe !== null ) {
    //Board.clear_pipe(spaces/* TODO: , space.next */)
    // TODO: Board.check_new_move(spaces, space)
  }

  return {
    spaces,
    currPipeEnd,
    isMouseDown: true,
  };
}

const updateStateOnMouseEnter = (row, col) => (prevState) => {
  const { spaces, isMouseDown, currPipeEnd } = prevState;
  if( !isMouseDown ) {
    return prevState;
  }
  const space = Board.getSpace(spaces, row, col);
  const currPipeSpace = Board.getSpace(spaces, currPipeEnd.row, currPipeEnd.col);

  space.pipe = currPipeSpace.pipe;
  const newPipeEnd = {row: row, col: col};

  return {
    spaces,
    currPipeEnd: newPipeEnd,
  };
}

const updateStateOnMouseUp = () => () => {
  return {
    isMouseDown: false,
    currPipeEnd: null,
  }
}

export default class Board extends Component {

  /*** STATIC METHODS ***/

  static createSpacesState(rows, cols, dots) {
    const spaces = new Array(rows);
    for( let i = 0; i < rows; i++ ) {
      spaces[i] = new Array(cols);
      for( let j = 0; j < cols; j++ ) {
        // TODO: add dots after spaces created
        spaces[i][j] = {
          row: i,
          col: j,
          dot: Board.getDotFromDots(dots, cols, i, j),
          pipe: null,
        };
      }
    }
    return spaces;
  }

  static getDotFromDots(dots, cols, row, col) {
    const spaceIndex = (row * cols) + col;
    if( dots === null || !(spaceIndex in dots) ) {
      return null;
    }
    return {color: dots[spaceIndex]};
  }

  static getSpace = (spaces, row, col) => {
    return spaces[row][col];
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
      currPipeEnd: null,
    };

    this.getSpaceDot = this.getSpaceDot.bind(this);
    this.getSpacePipe = this.getSpacePipe.bind(this);

    this.onMouseDown = this.onMouseDown.bind(this);
    this.onMouseEnter = this.onMouseEnter.bind(this);
    this.onMouseUp = this.onMouseUp.bind(this);
  }

  componentDidMount() {
    window.addEventListener('mouseup', this.onMouseUp);
    console.log(window);
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
        {boardRows}
      </div>
    );
  }
}
