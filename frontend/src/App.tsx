import React from 'react'
import './App.css'
import Search from './components/Search'
import { Pois } from './Interfaces'
import LeafletMap from './components/LeafletMap'
import PlaceCard from './components/PlaceCard'

function App() {
  // Points of interest list
  const [pois, setPois] = React.useState<Array<Pois>>([]);

  // Point of interest selected index
  const [poiIndex, setPoiIndex] = React.useState<number>(0);

  // State to hide or show the placecard 
  const [hidePlacecard, setHidePlacecard] = React.useState<boolean>(false);

  // State for the geocoded longitude and latitude
  const [coordinates, setCoordinates] = React.useState({lat: "43.6532", lon: "-79.3832"})

  // Loading state for backend
  const [isLoading, setLoading] = React.useState(false);

  // Pois not found state
  const [poiNotFound, setPoiNotFound] = React.useState(false);

  const [isInitialized, setisInitialized] = React.useState(false);

  React.useEffect(() => {
    if (!isInitialized) {
      // Skip the first render
      setisInitialized(true);
      return;
    }

    if (pois.length == 0) {
      setPoiNotFound(true);
    } else {
      setPoiNotFound(false);
    }
  }, [pois]);

  // Calculates distance w/ haversine formula
  const calcDistance = React.useCallback((lat1: number, lon1: number, lat2: number, lon2: number) => {
    if (lat1 === null || lat2 === null || lon1 === null || lon2 === null) {
      return 0;
    }

    const earthRadius = 6371
    const dLat = (lat2 - lat1) * (Math.PI / 180)
    const dLon = (lon2 - lon1) * (Math.PI / 180)
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * (Math.PI / 180)) *
        Math.cos(lat2 * (Math.PI / 180)) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    return earthRadius * c;
  }, []);

  const distance = React.useMemo(() => {
    if (pois.length > 0) {
      return calcDistance(Number(coordinates.lat), Number(coordinates.lon), pois[poiIndex].lat, pois[poiIndex].lon);
    }
    return 0;
  }, [pois, poiIndex, coordinates, calcDistance]);
  
  return (
    <>
      <Search setPois={setPois} setCoordinates={setCoordinates} coordinates={coordinates} setLoading={setLoading}/>
      <LeafletMap pois={pois} poiIndex={poiIndex} setPoiIndex={setPoiIndex} coordinates={coordinates} setHidePlacecard={setHidePlacecard}/>
      {
        pois.length > 0 &&

        <PlaceCard 
          key={`${pois[poiIndex].id}-${poiIndex}`} // Combine id and index to ensure uniqueness 
          poi={pois[poiIndex]} 
          distance={distance} 
          setHidden={setHidePlacecard} 
          hidden={hidePlacecard}/>
      }

      {
        isLoading && 

        <img src="./assets/loading.gif" alt="Loading..." className="loading"/>
      }

      {
        poiNotFound && 

        <div className="not-found">
          <div className="not-found-top">
            <span className="material-icons close-not-found" onClick={() => setPois([])}>close</span>
            <div className="not-found-body">No points of interest matching your query!</div>
          </div>
        </div>
      }
    </>
  )
}

export default App
