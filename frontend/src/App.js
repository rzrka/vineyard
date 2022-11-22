import React from 'react'
import VineyardMap from './components/VineyardMap'
import {HashRouter, Route, Link, Redirect, Routes, BrowserRouter} from 'react-router-dom'


function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <Routes>
      <Route exact path="/" element={<VineyardMap/>}/>
      </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
