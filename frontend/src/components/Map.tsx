import React from 'react';
import { MapContainer, TileLayer, Marker, Tooltip, useMap } from 'react-leaflet';
import L, { LatLngExpression } from 'leaflet'
import 'leaflet/dist/leaflet.css';
import { Coordinates, Pois } from '../Interfaces';


// Component which sets view based on the center and zoom
function UpdateMapView({ center }: { center: LatLngExpression }) {
  const map = useMap();
  map.setView(center);
  return null;
}

/**
 * Map Component
 *  
 * @param {Object} props - The component props.
 * @param {Array<Pois>} props.pois The points of interest
 * @param {number} props.poiIndex The index into the POI list
 * @param {React.Dispatch<React.SetStateAction<number>>} props.setPoiIndex The index into the POI array
 * @param {Coordinates} props.coordinates The coordinates to look around
 * @param {React.Dispatch<React.SetStateAction<boolean>>} props.setHidePlacecard Sets the state for hidden
 * @returns {JSX.Element} A React JSX element representing the NavBar Component, the navigation bar of the website
*/
export default function Map(props: {
    pois: Array<Pois>,
    poiIndex: number,
    setPoiIndex: React.Dispatch<React.SetStateAction<number>>,
    coordinates: Coordinates,
    setHidePlacecard: React.Dispatch<React.SetStateAction<boolean>>}) : JSX.Element {
        
    const [mapCenter, setMapCenter] = React.useState<LatLngExpression>([0,0]); // Sets center of the map to the coordinates of the given POI
    const zoomLevel = 14; // The zoom level of the map
   
     // Effect to update the map's center state when the user searches for a new location
     React.useEffect(() => {
        setMapCenter([Number(props.coordinates.lat), Number(props.coordinates.lon)]);
    }, [props.coordinates])
      
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
        <MapContainer center={mapCenter} zoom={zoomLevel} className="map">
          <UpdateMapView center={mapCenter}/>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {props.pois.map((pin, index) => (
            <Marker key={pin.id} position={[pin.lat, pin.lon]} icon={
                L.icon({
                    iconUrl: `./assets/${props.poiIndex == index ? "selected" : pin.tags.category}.png`,
                    iconSize: [50, 50],
                    iconAnchor: [25, 50],
                })} eventHandlers={{click: () => {
                        changeIndex(pin.id);
                        props.setHidePlacecard(false);
                    }}}>
                    <Tooltip>
                        <span>{pin.tags.name}</span>
                    </Tooltip>
            </Marker>
          ))}
        </MapContainer>
      );
}