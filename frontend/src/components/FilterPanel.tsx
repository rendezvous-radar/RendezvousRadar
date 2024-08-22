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
 * @returns {JSX.Element} A React JSX element representing the FilterPanel Component, the filter panel of the website
*/
export default function FilterPanel(
    props: {
        query: QueryType, 
        setQuery: React.Dispatch<React.SetStateAction<QueryType>>, 
        className: string, setSearch: React.Dispatch<React.SetStateAction<boolean>>
    }) : JSX.Element {    

    // Custom Radius State
    const [isCustomRadius, setIsCustomRadius] = React.useState<boolean>(false);

    const handleRadiusClick = (radius: string) => {
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
            radius: ""
        }));
    };

    const handleCustomRadiusInput = (event: ChangeEvent<HTMLInputElement>) => {
        props.setQuery(prevQuery => ({
            ...prevQuery,
            radius: event.target.value
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

        // Validate query fields
        if(props.query.radius !== "" &&
            !isNaN(Number(props.query.radius)) && 
            props.query.experience.length !== 0 && 
            props.query.activity.length !== 0 && 
            props.query.audience.length !== 0 && 
            props.query.time.length !== 0 && 
            props.query.season.length !== 0) {
                props.setSearch(true);
                console.log(Number(props.query.radius))
        }

        // TODO: Error Handling: Check that radius doesn't exceed maximum, display messages for missing specific queries
        else{
            console.log("Something's wrong")
        }

    }

    return ( 
        <div className={`filter-panel e${props.className}`}>
            <h3> Filters </h3>
            
            <div className="filter-inputs">
                <h4>Radius:</h4>
                {['1', '5', '10', '20'].map(radius => (
                    <button
                        key={radius}
                        className={props.query.radius == radius ? 'option-button selected' : 'option-button'}
                        onClick={() => handleRadiusClick(radius)}
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
                {['Romantic', 'Family-Friendly', 'Adventure', 'Relaxation', 'Cultural', 'Educational'].map(experience => (
                    <button
                        key={experience}
                        className={props.query.experience.includes(experience) ? 'option-button selected' : 'option-button'}
                        onClick={() => handleFilterClick('experience', experience)}
                    >
                        {experience}
                    </button>))}
            </div>

            <div className="filter-inputs">
                <h4>Activity:</h4>
                {['Outdoor', 'Indoor', 'Sports', 'Dining', 'Shopping', 'Entertainment'].map(activity => (
                    <button
                        key={activity}
                        className={props.query.activity.includes(activity) ? 'option-button selected' : 'option-button'}
                        onClick={() => handleFilterClick('activity', activity)}
                    >
                        {activity}
                    </button>))}
            </div>
            
            <div className="filter-inputs">
                <h4>Audience:</h4>
                {['Couples', 'Families', 'Groups', 'Solo'].map(audience => (
                    <button
                        key={audience}
                        className={props.query.audience.includes(audience) ? 'option-button selected' : 'option-button'}
                        onClick={() => handleFilterClick('audience', audience)}
                    >
                        {audience}
                    </button>))}
            </div>

            <div className="filter-inputs">
                <h4>Time:</h4>
                {['Morning', 'Afternoon', 'Evening', 'Night'].map(time => (
                    <button
                        key={time}
                        className={props.query.time.includes(time) ? 'option-button selected' : 'option-button'}
                        onClick={() => handleFilterClick('time', time)}
                    >
                        {time}
                    </button>))}
            </div>
            
            <div className="filter-inputs">
                <h4>Season:</h4>
                {['Winter', 'Spring', 'Summer', 'Fall'].map(season => (
                    <button
                        key={season}
                        className={props.query.season.includes(season) ? 'option-button selected' : 'option-button'}
                        onClick={() => handleFilterClick('season', season)}
                    >
                        {season}
                    </button>))}

                <button className='option-button filter' onClick={() => handleApplyFilterClick()}>Apply Filters</button>
            </div>
        </div>
    );
}