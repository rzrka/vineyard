import React from 'react'
import VineyardMap from './components/VineyardMap'
import {Route, Routes, BrowserRouter} from 'react-router-dom'


function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <Routes>
        {/* указывается какой компонент будет доступен по заданному пути */}
      <Route exact path="/" element={<VineyardMap/>}/>
      </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
