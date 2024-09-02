import React from 'react'
import './App.css'
import Search from './components/Search'
import { Pois } from './Interfaces'
import Map from './components/Map'
import PlaceCard from './components/PlaceCard'

function App() {
  // Points of interest list
  const [pois, setPois] = React.useState<Array<Pois>>([]);

  // Point of interest selected index
  const [poiIndex, setPoiIndex] = React.useState<number>(0);

  // State to hide or show the placecard 
  const [hidePlacecard, setHidePlacecard] = React.useState<boolean>(false);

  // State for the geocoded longitude and latitude
  const [coordinates, setCoordinates] = React.useState({lat: "43.796656647925026", lon: "-79.42200704246716"})

  // Calculates distance w/ haversine formula
  function calcDistance(lat1: number, lon1: number, lat2: number, lon2: number){
    const earthRadius = 6371
    const dLat = (lat2 - lat1) * (Math.PI / 180)
    const dLon = (lon2 - lon1) * (Math.PI / 180)
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * (Math.PI / 180)) *
        Math.cos(lat2 * (Math.PI / 180)) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    const distance = earthRadius * c;

    return distance;
}
  
  return (
    <>
      <Search setPois={setPois} setCoordinates={setCoordinates} coordinates={coordinates}></Search>
      <Map pois={pois} setPoiIndex={setPoiIndex} coordinates={coordinates} setHidePlacecard={setHidePlacecard}></Map>
      {
        pois.length > 0 ? 

        <PlaceCard key={pois[poiIndex].id} poi={pois[poiIndex]} distance={calcDistance(Number(coordinates.lat), Number(coordinates.lon), pois[poiIndex].lat, pois[poiIndex].lon)} setHidden={setHidePlacecard} hidden={hidePlacecard}></PlaceCard> :
        ""
      }
    </>
  )
}

export default App
