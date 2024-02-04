import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { Router, Route, Routes } from 'react-router-dom';
import './App.css'
import './tailwind.css';
import HomePage from './components/HomePage';
import PrivateArea from './components/PrivateArea';


function App() {
  return (
      <Routes>
        <Route path="*" element={<HomePage />} />
        <Route path="/PrivateArea" element={<PrivateArea />} />
      </Routes>
  );
}

export default App;