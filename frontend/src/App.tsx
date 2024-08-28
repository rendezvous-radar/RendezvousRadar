import React from 'react'
import './App.css'
import Search from './components/Search'
import { Pois } from './Interfaces'
import Map from './components/Map'

function App() {
  // Points of interest list
  const [pois, setPois] = React.useState<Array<Pois>>([]);

  // Point of interest selected index
  const [poiIndex, setPoiIndex] = React.useState<number>(0);
  
  return (
    <>
      <Search setPois={setPois}></Search>
      {pois.length > 0 ? 
        <Map pois={pois} setPoiIndex={setPoiIndex}></Map> :
        ""
      }
    </>
  )
}

export default App
