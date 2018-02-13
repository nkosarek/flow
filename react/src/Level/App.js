import React, { Component } from 'react';
import logo from '../logo.svg';
import './App.css';
import Board from './Board';

class App extends Component {

  render() {
    let boardRows = 3;
    let boardCols = 3;
    let dotLocations = {0:0, 4:0, 2:1, 3:1};
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


export default App;
