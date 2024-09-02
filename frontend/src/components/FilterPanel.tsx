import React, { ChangeEvent } from 'react';
import { QueryType } from '../Interfaces';

/**
 * FilterPanel Component
 *  
 * @param {Object} props - The component props.
 * @param {QueryType} props.query The query object for the api call
 * @param {React.Dispatch<React.SetStateAction<QueryType>>} props.setQuery Sets the query of the api call
 * @param {string} props.className Toggles visibility of the component
 * @param {React.Dispatch<React.SetStateAction<QueryType>>} props.setQuery Sets the query of the api call
 * @param {React.Dispatch<React.SetStateAction<QueryType>>} props.setFilterHidden Sets the Filter panel to visible/invisible state
 * @returns {JSX.Element} A React JSX element representing the FilterPanel Component, the filter panel of the website
*/
export default function FilterPanel(
    props: {
        query: QueryType, 
        setQuery: React.Dispatch<React.SetStateAction<QueryType>>, 
        className: string, 
        setSearch: React.Dispatch<React.SetStateAction<boolean>>,
        setFilterHidden: React.Dispatch<React.SetStateAction<boolean>>
    }) : JSX.Element {    

    // Custom Radius State
    const [isCustomRadius, setIsCustomRadius] = React.useState<boolean>(false);

    // Show Error Message State
    const [isWrong, setIsWrong] = React.useState<boolean>(false);

    // State to determine filter form versus AI search
    const [searchType, setSearchType] = React.useState<string>("manual");

    // AI Input
    const [aiInput, setAIInput] = React.useState<string>("");

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

    const handleFilterOptionClick = (event: React.MouseEvent<HTMLParagraphElement>) => {
        setSearchType(event.currentTarget.className);
    }

    const handleApplyFilterClick = () => {

        // Validate query fields
        if(props.query.radius !== 0 &&
            !isNaN(Number(props.query.radius)) && 
            Number(props.query.radius) <= 30 &&
            props.query.experience.length !== 0 && 
            props.query.activity.length !== 0 && 
            props.query.audience.length !== 0 && 
            props.query.time.length !== 0 && 
            props.query.season.length !== 0) {
                setIsWrong(false);
                props.setSearch(true);
                props.setFilterHidden(true);
        }

        else{
            setIsWrong(true);
            console.log("Something's wrong")
        }

    }

    // Sets address to current input value
    const handleAiInput = (event: ChangeEvent<HTMLInputElement>) => {
        setAIInput(event?.target.value);
    }

    //TODO: DO AI Query here!!
    const handleAIQuery = () => {
        // Call Backend and setQuery state

    }

    const activeStyle = {"borderBottom": "2px solid #368DFF", "color": "#368DFF"} // Sets the style of the active window

    return ( 
        <div className={`filter-panel ${props.className}`}>
            <div className="choose-window-filter"> 
                <p className="manual" onClick={handleFilterOptionClick} style={searchType === "manual" ? activeStyle : {}}>Manual Filters</p>
                <p className="ai-powered" onClick={handleFilterOptionClick} style={searchType === "ai-powered" ? activeStyle : {}}>AI Powered Search</p>
            </div>
            
            <div className={`${searchType === "manual" ? "visible-panel" : "invisible-panel"}`}>
                <div className="filter-inputs">
                    <h4>Radius:</h4>
                    {['1', '5', '10', '20'].map(radius => (
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

                <div className="filter-inputs">
                    <h4>Experience:</h4>
                    {['Romantic', 'Family-Friendly', 'Adventure', 'Relaxation', 'Cultural', 'Educational', 'Any'].map(experience => (
                        <button
                            key={experience}
                            className={props.query.experience.includes(experience.toLowerCase()) ? 'option-button selected' : 'option-button'}
                            onClick={() => handleFilterClick('experience', experience.toLowerCase())}
                        >
                            {experience}
                        </button>))}
                </div>

                <div className="filter-inputs">
                    <h4>Activity:</h4>
                    {['Outdoor', 'Indoor', 'Sports', 'Dining', 'Shopping', 'Entertainment', 'Any'].map(activity => (
                        <button
                            key={activity}
                            className={props.query.activity.includes(activity.toLowerCase()) ? 'option-button selected' : 'option-button'}
                            onClick={() => handleFilterClick('activity', activity.toLowerCase())}
                        >
                            {activity}
                        </button>))}
                </div>
                
                <div className="filter-inputs">
                    <h4>Audience:</h4>
                    {['Couples', 'Families', 'Groups', 'Solo', 'Any'].map(audience => (
                        <button
                            key={audience}
                            className={props.query.audience.includes(audience.toLowerCase()) ? 'option-button selected' : 'option-button'}
                            onClick={() => handleFilterClick('audience', audience.toLowerCase())}
                        >
                            {audience}
                        </button>))}
                </div>

                <div className="filter-inputs">
                    <h4>Time:</h4>
                    {['Morning', 'Afternoon', 'Evening', 'Night', 'Any'].map(time => (
                        <button
                            key={time}
                            className={props.query.time.includes(time.toLowerCase()) ? 'option-button selected' : 'option-button'}
                            onClick={() => handleFilterClick('time', time.toLowerCase())}
                        >
                            {time}
                        </button>))}
                </div>
                
                <div className="filter-inputs">
                    <h4>Season:</h4>
                    {['Winter', 'Spring', 'Summer', 'Fall', 'Any'].map(season => (
                        <button
                            key={season}
                            className={props.query.season.includes(season.toLowerCase()) ? 'option-button selected' : 'option-button'}
                            onClick={() => handleFilterClick('season', season.toLowerCase())}
                        >
                            {season}
                        </button>))}

                    <button className='option-button filter' onClick={() => handleApplyFilterClick()}>Apply Filters</button>
                </div>
                {
                    isWrong && 
                    <div className="error-msg">
                        <div>Select at least one filter per category, and a proper number that doesn't exceed 30 km for the radius.</div>
                        <span className="material-icons close-err" onClick={() => setIsWrong(false)}>close</span>
                    </div>
                }
            </div>

            <div className={`ai-panel ${searchType === "ai-powered" ? "visible-panel" : "invisible-panel"}`}>
                <input className="ai-search" placeholder='Give me some romantic date spots...' onChange={handleAiInput}></input>
                <button className="ai-button" onClick={handleAIQuery}><span className="material-icons searchIcon">search</span></button>
            </div>

        </div> 
        
    );
}