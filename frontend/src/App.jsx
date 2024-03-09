import { useState } from 'react';
import { Router, Route, Routes } from 'react-router-dom';
import ErrorBoundary from './components/ErrorBoundary'; // Import the ErrorBoundary component
import './App.css';
import './tailwind.css';
import HomePage from './components/HomePage';
import PrivateArea from './components/PrivateArea';

import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';

Chart.register(...registerables);

function App() {
  return (
    <ErrorBoundary>
      <Routes>
        <Route path="*" element={<HomePage />} />
        <Route path="/PrivateArea" element={<PrivateArea />} />
      </Routes>
    </ErrorBoundary>
  );
}

export default App;
