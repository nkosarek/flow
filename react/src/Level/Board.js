import React, { Component } from 'react';
import Space from './Space';

const getSpace = (spaces, row, col) => {
  return spaces[row][col];
}

const updateStateOnMouseDown = (row, col) => (prevState) => {
  const { spaces } = prevState;
  const space = getSpace(spaces, row, col);
  space.pipe = 'Q';
  return {
    spaces,
    isMouseDown: true
  };
}

const updateStateOnMouseEnter = (row, col) => (prevState) => {
  const { spaces, isMouseDown } = prevState;
  if( !isMouseDown ) {
    return prevState;
  }
  
  const space = getSpace(spaces, row, col);
  space.pipe = 'X';
  return {
    spaces,
  };
}

const updateStateOnMouseUp = () => (prevState) => {
  return {
    isMouseDown: false
  }
}

export default class Board extends Component {

  /*** STATIC METHODS ***/

  static createSpacesState(rows, cols, dots) {
    const spaces = new Array(rows);
    for( let i = 0; i < rows; i++ ) {
      spaces[i] = new Array(cols);
      for( let j = 0; j < cols; j++ ) {
        spaces[i][j] = {
          row: i,
          col: j,
          dot: Board.getDotFromDots(dots, cols, i, j),
          pipe: null
        };
      }
    }
    return spaces;
  }

  static getDotFromDots(dots, cols, row, col) {
    const spaceIndex = row*cols + col;
    if( dots === null || !(spaceIndex in dots) ) {
      return null;
    }
    return dots[spaceIndex];
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
      isMouseDown: false,
      spaces: Board.createSpacesState(rows, cols, dots)
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
    const {spaces} = this.state;
    const space = getSpace(spaces, row, col);
    return space.dot;
  }

  getSpacePipe(row, col) {
    const {spaces} = this.state;
    const space = getSpace(spaces, row, col);
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

    const boardRows = rowRange.map((row) =>
        <div
          key={row}
          className='board-row'
        >
          {
            colRange.map((col) =>
              <Space
                key={row*cols + col}
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
