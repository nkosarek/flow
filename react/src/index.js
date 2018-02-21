import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Level from './Level/Level';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<Level />, document.getElementById('root'));
registerServiceWorker();
