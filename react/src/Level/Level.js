import React, { Component } from 'react';
import logo from '../logo.svg';
import './Level.css';
import Board from './Board';
import TopLevelDisplay from './TopLevelDisplay';
import BottomLevelDisplay from './BottomLevelDisplay';
import Config from '../Config';

const {
  LEVEL_SETUP,
  LEVEL_SELECT_PATH,
  LEVEL_PATH_PREFIX,
} = Config;

// TODO: error handling
// TODO: updateStateOnMouseLeave (leave board)

const updateStateOnMouseDown = (row, col) => (prevState) => {
  const { spaces, pipeEndLoc, numMoves, lastColorAdvanced } = prevState;
  const space = Board.getSpace(spaces, row, col);
  let newPipeEndLoc = pipeEndLoc;
  let newNumMoves = numMoves;
  let newLastColorAdvanced = lastColorAdvanced;

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

  } else if( space.pipe !== null ) {
    Board.clearPipe(spaces, space.pipe.next)
    newPipeEndLoc = {row, col};
  }

  return {
    spaces,
    numMoves: newNumMoves,
    pipeEndLoc: newPipeEndLoc,
    isMouseDown: true,
    lastColorAdvanced: newLastColorAdvanced,
    levelComplete: false,
  };
}

// TODO: Clean this up
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
  const { spaces, pipeEndLoc, numMoves, lastColorAdvanced } = prevState;
  let newNumMoves = numMoves;
  let newLastColorAdvanced = lastColorAdvanced;

  if( pipeEndLoc !== null ) {
    const pipeEndSpace = Board.getSpace(spaces, pipeEndLoc.row, pipeEndLoc.col);
    const color = pipeEndSpace.pipe.color;

    // Check whether the pipe wasn't advanced past the first dot space
    if( pipeEndSpace.pipe.next === null && pipeEndSpace.pipe.last === null ) {
      Board.clearPipe(spaces, pipeEndLoc);

    // Check whether a new move was made or not
    } else if( color !== lastColorAdvanced ) {
      newNumMoves += 1;
      newLastColorAdvanced = color;
    }
  }

  const levelComplete = Board.checkLevelComplete(spaces);
  return {
    spaces,
    numMoves: newNumMoves,
    isMouseDown: false,
    pipeEndLoc: null,
    lastColorAdvanced: newLastColorAdvanced,
    levelComplete,
  }
}

const updateStateOnResetLevel = () => (prevState) => {
  let { spaces } = prevState;
  Board.clearBoard(spaces);

  return {
    spaces,
    numMoves: 0,
    isMouseDown: false,
    pipeEndLoc: null,
    lastColorAdvanced: null,
    levelComplete: false,
  }
};

/*****************************/
/********* COMPONENT *********/
/*****************************/

export default class Level extends Component {

  /*** NON-RENDER LIFECYCLE METHODS ***/

  constructor(props) {
    super(props);

    const {
      levelNumber = 0,
    } = this.props;

    if( !Number.isSafeInteger(levelNumber) ||
        levelNumber < 0 ||
        levelNumber >= LEVEL_SETUP.length ) {
      this.state = {
        mouseUpListenerRegistered: false,
        error: true,
      }
    } else {
      const { rows, cols, dots } = LEVEL_SETUP[levelNumber];

      this.state = {
        spaces: Board.createSpacesState(rows, cols, dots),
        numMoves: 0,
        isMouseDown: false,
        pipeEndLoc: null,
        lastColorAdvanced: null,
        levelComplete: false,
        mouseUpListenerRegistered: false,
        error: false,
      };
    }

    this.onMouseDown = this.onMouseDown.bind(this);
    this.onMouseEnter = this.onMouseEnter.bind(this);
    this.onMouseUp = this.onMouseUp.bind(this);
    this.onResetLevel = this.onResetLevel.bind(this);
  }

  componentDidMount() {
    if( !this.state.error ) {
      window.addEventListener('mouseup', this.onMouseUp);
      this.setState({ mouseUpListenerRegistered: true });
    }
  }

  componentWillUnmount() {
    if( this.state.mouseUpListenerRegistered ) {
      window.removeEventListener('mouseup', this.onMouseUp);
      this.setState({ mouseUpListenerRegistered: false });
    }
  }

  /*** EVENT HANDLERS ***/

  onMouseDown(row, col) {
    this.setState(updateStateOnMouseDown(row, col));
  }
  
  onMouseEnter(row, col) {
    this.setState(updateStateOnMouseEnter(row, col));
  }

  onMouseUp() {
    this.setState(updateStateOnMouseUp());
  }

  onResetLevel() {
    this.setState(updateStateOnResetLevel());
  }

  /*** RENDER ***/

  render() {
    const { levelNumber } = this.props;

    const {
      numMoves,
      spaces,
      error,
    } = this.state;

    const levelPathNumber = levelNumber + 1;
    let lastLevelPath = LEVEL_PATH_PREFIX;
    let nextLevelPath = LEVEL_PATH_PREFIX;

    if( levelPathNumber > 1 ) {
      lastLevelPath += levelPathNumber - 1;
    } else {
      lastLevelPath += levelPathNumber;
    }

    if( levelPathNumber < LEVEL_SETUP.length ) {
      nextLevelPath += levelPathNumber + 1;
    } else {
      nextLevelPath += levelPathNumber;
    }

    return (
      (error)
      ? <p>you done fucked up</p>
      : <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to Flow</h1>
        </header>
        <TopLevelDisplay
          numMoves={numMoves}
          levelSelectPath={LEVEL_SELECT_PATH}
        />
        <Board
          spaces={spaces}
          onMouseDown={this.onMouseDown}
          onMouseEnter={this.onMouseEnter}
        />
        <BottomLevelDisplay
          lastLevelPath={lastLevelPath}
          onResetLevel={this.onResetLevel}
          nextLevelPath={nextLevelPath}
        />
        {this.state.levelComplete
          ? <p>AHHHHHH</p>
          : null
        }
      </div>
    );
  }
}