import React from 'react';
import logo from './logo.svg';
import ReactDOM from "react-dom/client";
import Home from "./pages/Home";
import Grid from "./pages/Grid";
import NoPage from './pages/NoPage';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import './App.css';

function App() {
  return (
    <div className="App">
        <h1>Sudoku Solver</h1>
        <BrowserRouter>
        <Routes>
            <Route path="" element={<Home />} />
            <Route path="gridSolver" element={<Grid />} />
            <Route path="*" element={<NoPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
