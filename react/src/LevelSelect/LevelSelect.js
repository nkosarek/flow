import React from 'react';
import { Link } from 'react-router-dom';
import Config from '../Config';

const {
  LEVEL_PATH_PREFIX,
} = Config;

export default function LevelSelect(props) {
  return (
    <div>
      <p>LEVELS</p>
      <Link to={LEVEL_PATH_PREFIX + "1"}>
        <button>
          I'M LEVEL 1. GET AT ME.
        </button>
      </Link>
      <Link to={LEVEL_PATH_PREFIX + "2"}>
        <button>
          WELL I'M LEVEL 2. Get at him^
        </button>
      </Link>
      <Link to={LEVEL_PATH_PREFIX + "3"}>
        <button>
          3
        </button>
      </Link>
      <Link to={LEVEL_PATH_PREFIX + "4"}>
        <button>
          4
        </button>
      </Link>
      <Link to={LEVEL_PATH_PREFIX + "5"}>
        <button>
          5
        </button>
      </Link>
      <Link to={LEVEL_PATH_PREFIX + "6"}>
        <button>
          6
        </button>
      </Link>
    </div>
  );
};
