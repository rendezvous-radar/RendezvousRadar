import React from 'react';
import FilterPanel from './FilterPanel';
import NavBar from './NavBar';
import { CoordinateResponse, Coordinates, Pois, QueryType } from '../Interfaces';
import axios, { isAxiosError } from "axios";

/**
 * Search Component
 * @param {Object} props - The component props.
 * @param {React.Dispatch<React.SetStateAction<Array<Pois>>>} props.setPois Sets the list of pois
 * @param {Coordinates} props.coordinates Coordinates of the query
 * @param {React.Dispatch<React.SetStateAction<Coordinates>>} props.setCooordinates Sets the coordinates
 * @param {React.Dispatch<React.SetStateAction<boolean>>} props.setLoading Sets the loading state
 * @returns {JSX.Element} A React JSX element representing the Search Component, the search section of the website
*/
export default function Search(props: {
    setPois: React.Dispatch<React.SetStateAction<Array<Pois>>>,
    setCoordinates: React.Dispatch<React.SetStateAction<Coordinates>>,
    coordinates: Coordinates,
    setLoading: React.Dispatch<React.SetStateAction<boolean>>
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
    const [address, setAddress] = React.useState<string>("Toronto, Ontario, Canada");

    // Show Error Message State
    const [isWrong, setIsWrong] = React.useState<boolean>(false);

    // Error message
    const [errMsg, setErrMsg] = React.useState<string>("");

    function handleError(err : unknown) {
        if (isAxiosError(err) && err.response) {
            switch (err.response.status) {
                case 400:
                    setErrMsg("Invalid request. Please check your input and try again.");
                    break;
                case 401:
                    setErrMsg("You need to log in to perform this action.");
                    break;
                case 403:
                    setErrMsg("You do not have permission to access this resource.");
                    break;
                case 404:
                    setErrMsg("The requested resource was not found.");
                    break;
                case 500:
                    setErrMsg("An error occurred on our server. Please try again later.");
                    break;
                default:
                    setErrMsg("An unexpected error occurred. Please try again.");
            }
        }
    }

    async function getPois() {
        props.setLoading(true);
        try {
            const res = await axios.get(
                `${import.meta.env.VITE_BACKEND_LINK}/search-location/?lat=${props.coordinates.lat}&lon=${props.coordinates.lon}&radius=${query.radius * 1000}&experiences=${query.experience.join(',')}&activity=${query.activity.join(',')}&audience=${query.audience.join(',')}&seasons=${query.season.join(',')}&times=${query.time.join(',')}`
            );

            props.setPois(res.data.elements);

        } catch (err) {
            setIsWrong(true);
            handleError(err);
        } finally {
            props.setLoading(false);
        }
    }

    async function findCoordinates() {
        props.setLoading(true)
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
            setIsWrong(true);                
            handleError(err);
        } finally {
            props.setLoading(false);
        }
    }
    
    // Where the API is called
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
    }, [address]);

    return ( 
        <div className='search'>
            <NavBar setFilterHidden={setFilterHidden} setAddress={setAddress}/>
            <FilterPanel 
                query={query} 
                setQuery={setQuery} 
                setSearch={setSearch} 
                className={filterHidden ? 'filter-panel-hidden' : 'filter-panel-visible'} 
                setFilterHidden={setFilterHidden} 
                coordinates={props.coordinates} 
                setLoading={props.setLoading} 
                setPois={props.setPois}/>
            {
                isWrong && 
                <div className="error-msg">
                    <div>{errMsg}</div>
                    <span className="material-icons close-err" onClick={() => setIsWrong(false)}>close</span>
                </div>
            }
        </div>

    );
}