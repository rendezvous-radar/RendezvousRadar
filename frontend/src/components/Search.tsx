import React from 'react';
import FilterPanel from './FilterPanel';
import NavBar from './NavBar';
import { Coordinates, Pois, QueryType } from '../Interfaces';
import axios from "axios";

/**
 * Search Component
 * @param {Object} props - The component props.
 * @param {React.Dispatch<React.SetStateAction<Array<Pois>>>} props.setPois Sets the list of pois
 * @param {React.Dispatch<React.SetStateAction<Coordinates>>} props.setCooordinates Sets the coordinates
 * @returns {JSX.Element} A React JSX element representing the Search Component, the search section of the website
*/
export default function Search(props: {
    setPois: React.Dispatch<React.SetStateAction<Array<Pois>>>,
    setCoordinates: React.Dispatch<React.SetStateAction<Coordinates>>
    }) : JSX.Element {

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
    // TODO: Set isFound state, coordinates, and poi list
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