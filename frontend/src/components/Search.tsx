import React from 'react';
import FilterPanel from './FilterPanel';
import NavBar from './NavBar';
import { CoordinateResponse, Coordinates, Pois, QueryType } from '../Interfaces';
import axios from "axios";

/**
 * Search Component
 * @param {Object} props - The component props.
 * @param {React.Dispatch<React.SetStateAction<Array<Pois>>>} props.setPois Sets the list of pois
 * @param {React.Dispatch<React.SetStateAction<Coordinates>>} props.setCooordinates Sets the coordinates
 * @param {Coordinates} props.coordinates Coordinates of the query
 * @returns {JSX.Element} A React JSX element representing the Search Component, the search section of the website
*/
export default function Search(props: {
    setPois: React.Dispatch<React.SetStateAction<Array<Pois>>>,
    setCoordinates: React.Dispatch<React.SetStateAction<Coordinates>>,
    coordinates: Coordinates
    }) : JSX.Element {

    // State for opening and closing the filter panel menu
    const [filterHidden, setFilterHidden] = React.useState(true);

    // State for the type of query
    const [query, setQuery] = React.useState<QueryType>({
        radius: 0,
        experience: [],
        activity: [],
        audience: [],
        time: [],
        season: []
    })

    // State for user prompting a search
    const [search, setSearch] = React.useState<boolean>(false);

    // State for address string
    const [address, setAddress] = React.useState<string>("Vaughan, Ontario, Canada");

    async function getPois() {
        try {
            const res = await axios.get(
                `${import.meta.env.VITE_BACKEND_LINK}/search-location/?lat=${props.coordinates.lat}&lon=${props.coordinates.lon}&radius=${query.radius * 1000}&experiences=${query.experience.join(',')}&activity=${query.activity.join(',')}&audience=${query.audience.join(',')}&seasons=${query.season.join(',')}&times=${query.time.join(',')}`
            );

            props.setPois(res.data.elements)

        } catch (err) {
            // TODO: What to do with API call error
            console.log(err);
        }
        // SET POIs in list somewhere here
    }

    async function findCoordinates() {
        try {
            const res : CoordinateResponse = await axios.get(
                `${import.meta.env.VITE_BACKEND_LINK}/find-coords/?address=${address}`,
                {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                }
            );
            props.setCoordinates(res.data);

        } catch (err) {
            console.log(err);
        }
    }
    
    // Where the API is called, should add loading symbol, etc
    React.useEffect(() => {
        if (search) {

            if(query.radius == 0 
                || query.activity.length == 0 
                || query.experience.length == 0
                || query.audience.length == 0
                || query.time.length == 0
                || query.season.length == 0) {
                    setSearch(false)
                    return;
            }

            getPois();
            
        }
        
        setSearch(false);

    }, [search]);

    React.useEffect(() => {
        findCoordinates();
    }, [address])

    return ( 
        <div className='search'>
            <NavBar setFilterHidden={setFilterHidden} setAddress={setAddress}></NavBar>
            <FilterPanel query={query} setQuery={setQuery} setSearch={setSearch} className={filterHidden ? 'filter-panel-hidden' : 'filter-panel-visible'} setFilterHidden={setFilterHidden}></FilterPanel>
        </div>
    );
}