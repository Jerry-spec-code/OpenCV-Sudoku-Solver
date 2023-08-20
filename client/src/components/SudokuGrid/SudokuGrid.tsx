import React, { useState } from 'react';
import { Grid, TextField, styled } from '@mui/material';

const StyledGridContainer = styled(Grid)({
  flexGrow: 1,
  justifyContent: 'center',
  margin: 'auto',
});

const StyledGridItem = styled(Grid)(({ theme }) => ({
    padding: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '2.5em',
    height: '2.5em', // Adjust the height to make grids more square
    borderRadius: 0, // Make the corners sharper
    border: 'none',
}));

const getBorderStyling = (rowIndex : number, colIndex : number) => {
    const endIndex = 8;
    const thickBorder = '2.5px solid black';
    const thinBorder = '0.5px solid black';
    return { 
        borderTop: rowIndex % 3 == 0 ? thickBorder : thinBorder, 
        borderLeft: colIndex % 3 == 0 ? thickBorder : thinBorder, 
        borderBottom: rowIndex == endIndex ? thickBorder : 'none', 
        borderRight: colIndex == endIndex ? thickBorder : 'none', 
    };
}

type Props = {
  grid : number[][];
  setGrid : (args :  number[][]) => void;
  message : string;
  setMessage : (args : string) => void;
};

const SudokuGrid = ({grid, setGrid, message, setMessage} : Props) => {

  const handleCellChange = (row : number, col : number, value : number) => {
    const newGrid = [...grid];
    newGrid[row][col] = value < 10 ? value : 0;
    setGrid(newGrid);
  };

  const handleClearBoard = () => {
    const initialGrid = Array.from({ length: 9 }, () => Array.from({ length: 9 }, () => 0));
    setGrid(initialGrid);
    setMessage('');
  };

  return (
    <>
      <button onClick={handleClearBoard}>
          Clear board
      </button>
      <br />
      {message == '' ? <br /> : <p>{message}</p>}
    <StyledGridContainer container spacing={0}>
      {grid.map((row, rowIndex) => (
        <Grid container item key={rowIndex} justifyContent="center">
          {row.map((cellValue, colIndex) => (
            <StyledGridItem item key={colIndex}>
              <TextField
                variant="outlined"
                size="small"
                value={cellValue === 0 ? '' : cellValue}
                onChange={(e) => handleCellChange(rowIndex, colIndex, +e.target.value || 0)}
                inputProps={{ style: { textAlign: 'center' } }}
                sx = {getBorderStyling(rowIndex, colIndex)}
              />
            </StyledGridItem>
          ))}
        </Grid>
      ))}
    </StyledGridContainer>
    </>
  );
};

export default SudokuGrid;
