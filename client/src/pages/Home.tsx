import React, { useEffect, useState } from "react";
import { Outlet, Link } from "react-router-dom";
import Btn from "../components/Button/Button";
import ROUTES from "../config/api";
import SudokuGrid from "../components/SudokuGrid/SudokuGrid";
import axios, { AxiosResponse, AxiosError }  from 'axios';

type Solution = {
    valid : boolean;
    solution : number[][];
    message : string;
};

const initialGrid = Array.from({ length: 9 }, () => Array.from({ length: 9 }, () => 0));

const Home = () => {
    
    const [solve, setSolve] = useState(false);
    const [solveGrid, setSolveGrid] = useState(false);
    const [data, setData] = useState<Solution | null>(null);
    const [selectedImage, setSelectedImage] = useState<File | null>(null);
    const [message, setMessage] = useState('');
    const [grid, setGrid] = useState(initialGrid);
    const [showGrid, setShowGrid] = useState(false);
    const [error, setError] = useState('');

    const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (file) {
        setSelectedImage(file);
      }
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
                            setGrid(data.solution);
                            setShowGrid(true);
                        }
                        setMessage(data.message);
                        setError('');
                    }
                    else {
                        setError(data.error);
                        setData(null);
                    }
                    setSolve(false);
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
                            if (data.valid) {
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
    }, [solveGrid]);

    const ShowGrid = () => {
        return <>
            <SudokuGrid grid={grid} setGrid={setGrid} message={message} setMessage={setMessage}/>
            <br />
            <Btn clicked={solveGrid} setClicked={setSolveGrid} text={"Solve Grid!"}/>
        </>
    }

    return <div>
        <Link to="/gridSolver">Fill in the grid instead</Link>
        <br /><br />
        <input style={{ marginLeft: '75px' }} type="file" accept="image/*" onChange={handleImageChange} />
        <br /><br />
        <Btn clicked={solve} setClicked={setSolve} text={'Solve!'} />
        {error != '' && <p>{error}</p>}
        <br />
        {showGrid && ShowGrid()}
    </div>
};
  
export default Home;