import React, { ChangeEvent } from 'react';
import { Coordinates, Pois, QueryType } from '../Interfaces';
import axios, { isAxiosError } from 'axios';

// Reusable filter options data
const FILTER_OPTIONS = {
    experience: ['Romantic', 'Family-Friendly', 'Adventure', 'Relaxation', 'Cultural', 'Educational', 'Any'],
    activity: ['Outdoor', 'Indoor', 'Sports', 'Dining', 'Shopping', 'Entertainment', 'Any'],
    audience: ['Couples', 'Families', 'Groups', 'Solo', 'Any'],
    time: ['Morning', 'Afternoon', 'Evening', 'Night', 'Any'],
    season: ['Winter', 'Spring', 'Summer', 'Fall', 'Any']
};

/**
 * FilterPanel Component
 *  
 * @param {Object} props - The component props.
 * @param {QueryType} props.query The query object for the api call
 * @param {React.Dispatch<React.SetStateAction<QueryType>>} props.setQuery Sets the query of the api call
 * @param {string} props.className Toggles visibility of the component
 * @param {React.Dispatch<React.SetStateAction<QueryType>>} props.setQuery Sets the query of the api call
 * @param {React.Dispatch<React.SetStateAction<QueryType>>} props.setFilterHidden Sets the Filter panel to visible/invisible state
 * @param {Coordinates} props.coordinates Coordinates of the query
 * @param {React.Dispatch<React.SetStateAction<boolean>>} props.setLoading Sets the loading state
 * @param {React.Dispatch<React.SetStateAction<Array<Pois>>>} props.setPois Sets the list of pois
 * @returns {JSX.Element} A React JSX element representing the FilterPanel Component, the filter panel of the website
*/
export default function FilterPanel(
    props: {
        query: QueryType, 
        setQuery: React.Dispatch<React.SetStateAction<QueryType>>, 
        className: string, 
        setSearch: React.Dispatch<React.SetStateAction<boolean>>,
        setFilterHidden: React.Dispatch<React.SetStateAction<boolean>>,
        coordinates: Coordinates,
        setLoading: React.Dispatch<React.SetStateAction<boolean>>,
        setPois: React.Dispatch<React.SetStateAction<Array<Pois>>>
    }) : JSX.Element {    

    // Custom Radius State
    const [isCustomRadius, setIsCustomRadius] = React.useState<boolean>(false);

    // Show Error Message State
    const [isWrong, setIsWrong] = React.useState<boolean>(false);

    // Error message
    const [errMsg, setErrMsg] = React.useState<string>("");

    // State to determine filter form versus AI search
    const [searchType, setSearchType] = React.useState<string>("manual");

    // AI Input
    const [aiInput, setAIInput] = React.useState<string>("");

    // Ai Radius
    const [aiRadius, setAiRadius] = React.useState<number>(1000);

    const handleRadiusClick = (radius: number) => {
        props.setQuery(prevQuery => ({
            ...prevQuery,
            radius: radius
        }));
        setIsCustomRadius(false);
    };

    const handleIsCustomRadius = () => {
        setIsCustomRadius(prevState => !prevState)
        props.setQuery(prevQuery => ({
            ...prevQuery,
            radius: 0
        }));
    };

    const handleCustomRadiusInput = (event: ChangeEvent<HTMLInputElement>) => {
        props.setQuery(prevQuery => ({
            ...prevQuery,
            radius: Number(event.target.value)
        }));
    };

    const handleFilterClick = (filterType: 'experience' | 'activity' | 'audience' | 'time' | 'season', value: string) => {
        props.setQuery(prevQuery => ({
            ...prevQuery,
            [filterType]: prevQuery[filterType].includes(value)
                ? prevQuery[filterType].filter((item: string) => item !== value)
                : [...prevQuery[filterType], value]
        }));
    };

    const handleApplyFilterClick = () => {
        const isValid = props.query.radius !== 0 &&
        !isNaN(Number(props.query.radius)) && 
        Number(props.query.radius) <= 20 &&
        props.query.experience.length !== 0 && 
        props.query.activity.length !== 0 && 
        props.query.audience.length !== 0 && 
        props.query.time.length !== 0 && 
        props.query.season.length !== 0;

        // Validate query fields
        if(isValid) {
            setIsWrong(false);
            props.setSearch(true);
            props.setFilterHidden(true);
        }
        
        else{
            setErrMsg("Select at least one filter per category, and a proper number that doesn't exceed 20 km for the radius.");
            setIsWrong(true);
        }

    }

    // Sets address to current input value
    const handleAiInput = (event: ChangeEvent<HTMLInputElement>) => {
        setAIInput(event?.target.value);
    }

    const handleAiRadius = (event: ChangeEvent<HTMLSelectElement>) => {
        setAiRadius(Number(event?.target.value))
    } 

    async function handleAIQuery() {
        props.setFilterHidden(true);
        props.setLoading(true);
        setIsWrong(false);
        try {
            const res = await axios.get(
                `${import.meta.env.VITE_BACKEND_LINK}/ai-search/?lat=${props.coordinates.lat}&lon=${props.coordinates.lon}&radius=${aiRadius}&prompt=${aiInput}`
            )
            props.setPois(res.data.elements);
        } catch (err : unknown) {
            setIsWrong(true);
            props.setFilterHidden(false);
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
        } finally {
            props.setLoading(false);
        }
    }

    const activeStyle = {"borderBottom": "2px solid #368DFF", "color": "#368DFF"} // Sets the style of the active window

    // Helper function for rendering filter buttons
    const renderFilterButtons = (filterType: 'experience' | 'activity' | 'audience' | 'time' | 'season') => {
        return FILTER_OPTIONS[filterType].map((option) => (
        <button
            key={option}
            className={props.query[filterType].includes(option.toLowerCase()) ? 'option-button selected' : 'option-button'}
            onClick={() => handleFilterClick(filterType, option.toLowerCase())}
        >
            {option}
        </button>
        ));
    };
  
    return ( 
        <div className={`filter-panel ${props.className}`}>
            <div className="choose-window-filter"> 
                <p className="manual" onClick={() => setSearchType('manual')} style={searchType === "manual" ? activeStyle : {}}>Manual Filters</p>
                <p className="ai-powered" onClick={() => setSearchType('ai-powered')} style={searchType === "ai-powered" ? activeStyle : {}}>AI Powered Search</p>
            </div>

            {/* Manual Filters */}
            <div className={`${searchType === "manual" ? "visible-panel" : "invisible-panel"}`}>
                <div className="filter-inputs">
                    <h4>Radius:</h4>
                    {['1', '5', '10'].map(radius => (
                        <button
                            key={radius}
                            className={props.query.radius == Number(radius) ? 'option-button selected' : 'option-button'}
                            onClick={() => handleRadiusClick(Number(radius))}
                        >
                            {radius} km
                        </button>
                    ))}
                    <button
                        key="custom"
                        className={isCustomRadius ? 'option-button selected' : 'option-button'}
                        onClick={handleIsCustomRadius}
                    >
                        Custom
                    </button>

                    {isCustomRadius && 
                        <div className="custom-radius">
                            <h4> Enter Radius: </h4>
                            <input onChange={handleCustomRadiusInput}></input>
                            <h4> km </h4>
                        </div>
                    }
                </div>
                {['experience', 'activity', 'audience', 'time', 'season'].map((filterType) => (
                    <div className="filter-inputs" key={filterType}>
                    <h4>{filterType.charAt(0).toUpperCase() + filterType.slice(1)}:</h4>
                    {renderFilterButtons(filterType as 'experience' | 'activity' | 'audience' | 'time' | 'season')}
                    </div>
                ))}

                <button className='option-button filter' onClick={() => handleApplyFilterClick()}>Apply Filters</button>
            </div>

            {/* AI Search */}
            <div className={`ai-panel ${searchType === "ai-powered" ? "visible-panel" : "invisible-panel"}`}>
                <div className='ai-form'>
                    <input className="ai-search" placeholder='Give me some fun activities to do...' onChange={handleAiInput}></input>
                    <select id="range" name="range" className="ai-select" onChange={handleAiRadius}>
                        <option value="1000">1 km</option>
                        <option value="5000">5 km</option>
                        <option value="10000">10 km</option>
                    </select>
                    <button className="ai-button" onClick={handleAIQuery}><span className="material-icons searchIcon">search</span></button>
                </div>
            </div>

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