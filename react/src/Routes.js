import React from 'react';
import {
  BrowserRouter as Router,
  Route
} from 'react-router-dom';

import Home from './Home/Home';
import LevelSelect from './LevelSelect/LevelSelect'
import Level from './Level/Level';

export default function Routes(props) {
  return (
    <Router {...props}>
      <div>
        <Route exact path="/" component={Home} />
        <Route exact path="/level-select" component={LevelSelect} />
        <Route path="/level/:levelNumber" component={LevelWrapper} />
      </div>
    </Router>
  );
}

const LevelWrapper = ({ match }) => {
  const levelNumber = match.params.levelNumber-1;
  return (
    <Level key={levelNumber} levelNumber={levelNumber} />
  );
}