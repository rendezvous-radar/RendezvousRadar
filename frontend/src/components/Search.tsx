import React from 'react';
import FilterPanel from './FilterPanel';
import NavBar from './NavBar';
import { QueryType } from '../Interfaces';
import axios from "axios";

/**
 * Search Component
 *  
 * @returns {JSX.Element} A React JSX element representing the Search Component, the search section of the website
*/
export default function Search() : JSX.Element {
    // State for the geocoded longitude and latitude
    const [coordinates, setCoordinates] = React.useState({lat: "43.796656647925026", lon: "-79.42200704246716"})

    // Location found state
    const [isFound, setIsFound] = React.useState(false);

    // State for opening and closing the filter panel menu
    const [filterHidden, setFilterHidden] = React.useState(true);

    // State for the type of query
    const [query, setQuery] = React.useState<QueryType>({
        radius: "",
        experience: [],
        activity: [],
        audience: [],
        time: [],
        season: []
    })

    // State for user prompting a search
    const [search, setSearch] = React.useState<boolean>(false);

    // State for address string
    const [address, setAddress] = React.useState<string>("");

    // Geocodes the Location with the Nominatim API
    async function geocode (addr : string) {
        try {
            const response = await axios.get(`https://nominatim.openstreetmap.org/search?q=${addr}&format=json`, {
                headers: {
                    referer: "https://jinhakimgh.github.io/Basketball-Court-Finder", //TODO: Change this
                    "User-Agent": "Rendezvous-Radar" 
                }
            });

            if(response.data.length > 0) {
                const {lat, lon} = response.data[0];
                setCoordinates({lat: lat, lon: lon});
                setIsFound(true);
            } else {
                setIsFound(false);
            }

        } catch (err) {
            console.error("Error geocoding location", err);
        }
    }

    // POI Fetching: Key_value is the array of tuples of the key value pairs generated from the backend
    // TODO: Update
    const fetchPOIs = async (key_value: Array<Array<string>>) => {
        try {
          const latitude = coordinates.lat;
          const longitude = coordinates.lon; 

          let query_string = "[out:json];(";

          for (let i = 0; i < key_value.length; i += 1) {
            if (i == key_value.length - 1) {
                query_string = query_string.concat(`way(around:${query.radius},${latitude},${longitude})["${key_value[i][0]}"=${key_value[i][1]}];);out center;`)
            }
            else {
                query_string = query_string.concat(`way(around:${query.radius},${latitude},${longitude})["${key_value[i][0]}"=${key_value[i][1]}];`)
            }
          }
  
          const response = await axios.get('https://overpass-api.de/api/interpreter', {
            params: {
              data: query_string,
            },
          });

          // Sorts the basketball courts by distance
          //setBasketballCourts(sortCourts(response, latitude, longitude));
          
        } catch (error) {
          console.error('Error fetching Basketball Courts:', error);
        }
    }
    
    // Where the API is called, should add loading symbol, etc
    // TODO: Search is only set by the filter-options, we must also add an additional state for the Model's output
    React.useEffect(() => {
        if (search) {
            // Geocode the address
            geocode(address);
        }

        setSearch(false);

    }, [search, address]);

    return ( 
        <div className='search'>
            <NavBar setFilterHidden={setFilterHidden} setAddress={setAddress}></NavBar>
            <FilterPanel query={query} setQuery={setQuery} setSearch={setSearch} className={filterHidden ? 'filter-panel-hidden' : 'filter-panel-visible'}></FilterPanel>
        </div>
    );
}