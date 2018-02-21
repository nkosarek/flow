import React, { Component } from 'react';
import logo from '../logo.svg';
import './Level.css';
import Board from './Board';

export default class Level extends Component {

  render() {
    const boardRows = 3;
    const boardCols = 3;
    const dotLocations = [[0,0,1,1], [1,0,0,2]];
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to Flow</h1>
        </header>
        <Board
          rows={boardRows}
          cols={boardCols}
          dots={dotLocations}
        />
      </div>
    );
  }
}