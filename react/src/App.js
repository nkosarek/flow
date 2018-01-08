import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to Flow</h1>
        </header>
        <Board
          level="0"
          className="Board"
        />
      </div>
    );
  }
}

class Board extends Component {
  render() {
    const {
      level = '0',
      className = '',
    } = this.props;

    let rows = [];

    return (
      <div>
      </div>
    );
  }
}

const BoardRow = ({columns, dots, children}) =>
  <BoardSpace />

const BoardSpace = ({dot, fill, children}) =>
  <button />

export default App;
