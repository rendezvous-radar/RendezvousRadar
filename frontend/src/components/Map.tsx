import React from 'react';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import L, { LatLngExpression } from 'leaflet'
import 'leaflet/dist/leaflet.css';
import { Pois } from '../Interfaces';

/**
 * Map Component
 *  
 * @param {Object} props - The component props.
 * @param {Array<Pois>} props.pois The points of interest
 * @param {React.Dispatch<React.SetStateAction<number>>} props.setPoiIndex Sets the address of the API call
 * @returns {JSX.Element} A React JSX element representing the NavBar Component, the navigation bar of the website
*/
export default function Map(props: {
    pois: Array<Pois>,
    setPoiIndex: React.Dispatch<React.SetStateAction<number>> }) : JSX.Element {
        
    const [mapCenter, setMapCenter] = React.useState<LatLngExpression>([0,0]); // Sets center of the map to the coordinates of the given POI
    const [key, setKey] = React.useState(0); // Key property to force map container update
    const zoomLevel = 12; // The zoom level of the map
   
     // Effect to update the map's center state when the user searches for a new location
     React.useEffect(() => {
        if(props.pois.length > 0){
          setMapCenter([props.pois[0].lat, props.pois[0].lon]);
          setKey(prevKey => prevKey + 1);
        }
      }, [props.pois])
      
      // Updates the index when clicking into another place
      function changeIndex(id: string){
          let newIndex = 0
  
          for(let i = 0; i < props.pois.length; i++){
              if(props.pois[i].id == id){
                  newIndex = i;
                  break;
              }
          }
  
  
          props.setPoiIndex(newIndex)
      }
    
      return (
        <MapContainer key={key} center={mapCenter} zoom={zoomLevel} className="map">
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {props.pois.map(pin => (
            <Marker key={pin.id} position={[pin.lat, pin.lon]} icon={
                L.icon({
                    iconUrl: `./assets/${pin.type}.png`,
                    iconSize: [30, 30],
                    iconAnchor: [12, 41],
                })} eventHandlers={{click: () => changeIndex(pin.id)}}>
            </Marker>
          ))}
        </MapContainer>
      );
}