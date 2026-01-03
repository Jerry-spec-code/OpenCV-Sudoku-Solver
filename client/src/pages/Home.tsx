import React, { useEffect, useState, useRef } from "react";
import { Outlet, Link } from "react-router-dom";
import Btn from "../components/Button/Button";
import ROUTES from "../config/api";
import SudokuGrid from "../components/SudokuGrid/SudokuGrid";
import axios, { AxiosResponse, AxiosError }  from 'axios';
import { Grid } from "@mui/material";

type UpdateOperation = 
    | ['add', number, number, number]
    | ['delete', number, number, number];

type Solution = {
    valid : boolean;
    solution : number[][];
    original? : string[][];
    message : string;
    updates? : UpdateOperation[];
};

const initialGrid = Array.from({ length: 9 }, () => Array.from({ length: 9 }, () => 0));

const Home = () => {
    
    const [solve, setSolve] = useState(false);
    const [solveGrid, setSolveGrid] = useState(false);
    const [data, setData] = useState<Solution | null>(null);
    const [selectedImage, setSelectedImage] = useState<File | null>(null);
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [message, setMessage] = useState('');
    const [grid, setGrid] = useState(initialGrid);
    const [showGrid, setShowGrid] = useState(false);
    const [error, setError] = useState('');
    const [isAnimating, setIsAnimating] = useState(false);
    const [highlightedCell, setHighlightedCell] = useState<{row: number, col: number} | null>(null);
    const timeoutRef = useRef<NodeJS.Timeout | null>(null);

    const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (file) {
        setSelectedImage(file);

        // Create a URL for the selected image
        const imageURL = URL.createObjectURL(file);
        setImagePreview(imageURL);
      }
    };

    const convertStringsToNumbers = (array: string[][]): number[][] => {
        return array.map(row => row.map(cell => parseInt(cell)));
    }

    const startAnimation = (updates: UpdateOperation[], initialGridState: number[][]) => {
        if (!updates || updates.length === 0) {
            return;
        }

        setIsAnimating(true);
        let currentGrid = initialGridState.map(row => [...row]);
        let updateIndex = 0;

        const processNextUpdate = () => {
            if (updateIndex >= updates.length) {
                setIsAnimating(false);
                setSolve(false);
                setHighlightedCell(null);
                timeoutRef.current = null;
                return;
            }

            const update = updates[updateIndex];
            // Highlight the cell being updated
            setHighlightedCell({ row: update[1], col: update[2] });
            
            // Create a completely new array structure to ensure React detects the change
            const newGrid = currentGrid.map((row, rowIdx) => 
                row.map((cell, colIdx) => {
                    if (update[0] === 'add' && update[1] === rowIdx && update[2] === colIdx) {
                        return update[3];
                    } else if (update[0] === 'delete' && update[1] === rowIdx && update[2] === colIdx) {
                        return 0;
                    }
                    return cell;
                })
            );

            currentGrid = newGrid;
            // Create a deep copy to ensure React detects the change
            const updatedGrid = JSON.parse(JSON.stringify(newGrid));
            setGrid(updatedGrid);
            updateIndex++;
            
            timeoutRef.current = setTimeout(processNextUpdate, 200);
        };

        processNextUpdate();
    };

    useEffect(() => {
        if (solve) {
            if (selectedImage) {
                const formData = new FormData();
                formData.append('image', selectedImage);
          
                axios.post(ROUTES.imageSolver, formData)
                  .then((response : AxiosResponse) => {
                    const data = response.data;
                    if (data.status === "success") {
                        setData(data);
                        if (data.valid) {
                            const originalGrid = convertStringsToNumbers(data.original);
                            setGrid(originalGrid);
                            setShowGrid(true);
                            if (data.updates && data.updates.length > 0) {
                                // Start animation after a small delay to ensure grid is rendered
                                setTimeout(() => {
                                    startAnimation(data.updates, originalGrid);
                                }, 100);
                            }
                        }
                        setMessage(data.message);
                        setError('');
                    }
                    else {
                        setError(data.error);
                        setData(null);
                    }
                  })
                  .catch((error : AxiosError) => {
                    console.error(error);
                    setError(error.message);
                    setSolve(false);
                  });
              }
              else {
                setError('No selected image!');
                setSolve(false);
              }
        }
    }, [solve]);

    useEffect(() => {
        if (solveGrid) {
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify({ grid : grid })
            }
            const fetchData = async () => {
                await fetch(ROUTES.gridSolver, requestOptions)
                    .then((res) => res.json())
                    .then((data) => {
                        console.log(data);
                        if (data.status === "success") {
                            setData(data);
                            if (data.valid && data.updates && data.updates.length > 0) {
                                // Start animation with updates
                                const initialGridCopy = grid.map(row => [...row]);
                                setGrid(initialGridCopy);
                                setTimeout(() => {
                                    startAnimation(data.updates, initialGridCopy);
                                }, 100);
                            } else if (data.valid) {
                                setGrid(data.solution);
                            }
                            setMessage(data.message);
                        }
                        else {
                            setData(null);
                        }
                        setSolveGrid(false);
                    })
            }
            fetchData();
        }

        // Cleanup function to clear timeout on unmount or when solveGrid changes
        return () => {
            if (timeoutRef.current) {
                clearTimeout(timeoutRef.current);
                timeoutRef.current = null;
            }
        };
    }, [solveGrid]);

    const ShowGrid = () => {
        return <>
        <Grid container spacing={1}>
            <Grid item xs={4}>
                <br /><br /><br /><br />
                {imagePreview && <img src={imagePreview} alt="Preview" style={{ maxWidth: '100%', height: 'auto' }}/>}
            </Grid>
            <Grid item xs={4}>
                <SudokuGrid grid={grid} setGrid={setGrid} message={message} setMessage={setMessage} highlightedCell={highlightedCell}/>
                <br />
                <Btn clicked={solveGrid || isAnimating} setClicked={setSolveGrid} text={"Solve Grid!"}/>
            </Grid>
        </Grid>
        </>
    }

    return <div>
        <Link to="/gridSolver">Fill in the grid instead</Link>
        <br />
        <p>Upload an image of an unsolved sudoku puzzle</p>
        <input style={{ marginLeft: '75px' }} type="file" accept="image/*" onChange={handleImageChange} />
        <br /><br />
        <Btn clicked={solve} setClicked={setSolve} text={'Solve!'} />
        {error != '' && <p>{error}</p>}
        <br />
        {showGrid && ShowGrid()}
    </div>
};
  
export default Home;