import React from 'react';
import { MapContainer, TileLayer, Marker, Tooltip } from 'react-leaflet';
import L, { LatLngExpression } from 'leaflet'
import 'leaflet/dist/leaflet.css';
import { Coordinates, Pois } from '../Interfaces';

/**
 * Map Component
 *  
 * @param {Object} props - The component props.
 * @param {Array<Pois>} props.pois The points of interest
 * @param {React.Dispatch<React.SetStateAction<number>>} props.setPoiIndex Sets the address of the API call
 * @param {Coordinates} props.coordinates The coordinates to look around
 * @param {React.Dispatch<React.SetStateAction<boolean>>} props.setHidePlacecard Sets the state for hidden
 * @returns {JSX.Element} A React JSX element representing the NavBar Component, the navigation bar of the website
*/
export default function Map(props: {
    pois: Array<Pois>,
    setPoiIndex: React.Dispatch<React.SetStateAction<number>>,
    coordinates: Coordinates,
    setHidePlacecard: React.Dispatch<React.SetStateAction<boolean>>}) : JSX.Element {
        
    const [mapCenter, setMapCenter] = React.useState<LatLngExpression>([0,0]); // Sets center of the map to the coordinates of the given POI
    const [key, setKey] = React.useState(0); // Key property to force map container update
    const zoomLevel = 12; // The zoom level of the map
   
     // Effect to update the map's center state when the user searches for a new location
     React.useEffect(() => {
        setMapCenter([Number(props.coordinates.lat), Number(props.coordinates.lon)]);
        setKey(prevKey => prevKey + 1);
    }, [props.pois, props.coordinates])
      
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
          setMapCenter([props.pois[newIndex].lat, props.pois[newIndex].lon]) // Updates center of the map to the marker selected
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
                })} eventHandlers={{click: () => {
                        changeIndex(pin.id);
                        props.setHidePlacecard(false);
                    }}}>
                    <Tooltip>
                        <span>{pin.name}</span>
                    </Tooltip>
            </Marker>
          ))}
        </MapContainer>
      );
}