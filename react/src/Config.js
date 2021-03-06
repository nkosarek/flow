const Config = {
  LEVEL_SETUP: [
    {
      rows: 3,
      cols: 3,
      dots: [[0,0,1,1], [1,0,0,2]],
    },
    {
      rows: 5,
      cols: 5,
      dots: [[0,0,3,1], [0,4,4,3], [1,2,1,4], [3,3,4,0]],
    },
    {
      rows: 6,
      cols: 6,
      dots: [[0,0,1,5], [1,4,4,4], [4,1,5,5], [4,3,5,4]],
    },
    {
      rows: 7,
      cols: 7,
      dots: [[0,1,5,4], [0,3,1,1], [0,4,2,4], [0,6,4,4], [1,4,5,1]],
    },
    {
      rows: 8,
      cols: 8,
      dots: [[0,0,6,1], [1,0,2,5], [1,6,6,6], [2,6,3,5], [5,4,7,3]],
    },
    {
      rows: 12,
      cols: 12,
      dots: [[2,2,3,7], [2,7,8,3], [4,5,11,7], [4,6,11,5], [4,7,11,4], [6,6,11,0], [8,2,10,5]],
    }
  ],
  
  LEVEL_SELECT_PATH: '/level-select',
  LEVEL_PATH_PREFIX: '/level/',
}

export default Config;