import React from 'react'
import Map from './components/Map'
import {HashRouter, Route, Link, Redirect, Routes, BrowserRouter} from 'react-router-dom'


function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <Routes>
      <Route exact path="/" element={<Map/>}/>
      </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
