import React from 'react';
import FilterPanel from './FilterPanel';
import NavBar from './NavBar';
import { Pois, QueryType } from '../Interfaces';
import axios from "axios";

/**
 * Search Component
 *  
 * @returns {JSX.Element} A React JSX element representing the Search Component, the search section of the website
*/
export default function Search(props: {
    setPois: React.Dispatch<React.SetStateAction<Array<Pois>>>
    }) : JSX.Element {
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

    
    // Where the API is called, should add loading symbol, etc
    // TODO: Search is only set by the filter-options, we must also add an additional state for the Model's output
    // TODO: Call backend
    React.useEffect(() => {
        if (search) {
            // CALL BACKEND
            console.log("HELLO")

            // SET POIs in list somewhere here
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