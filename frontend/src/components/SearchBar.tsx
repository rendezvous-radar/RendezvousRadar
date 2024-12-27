import React from "react";
import { ChangeEvent } from "react";

/**
 * SearchBar Component
 *  
 * @param {Object} props - The component props.
 * @param {React.Dispatch<React.SetStateAction<string>>} props.setAddress Sets the address of the api call
 * @returns {JSX.Element} A React JSX element representing the SearchBar Component, the search bar of the website
*/
export default function SearchBar(props: {setAddress: React.Dispatch<React.SetStateAction<string>>}) : JSX.Element {

    // Input value
    const [inputValue, setInputValue] = React.useState<string>("Toronto, Ontario, Canada");

    // Handling Submission we only want to set the address once the form is submitted, reducing API calls
    const handleSubmit = React.useCallback(() => {
        props.setAddress(inputValue);
    }, [inputValue, props]);

    // Sets address to current input value
    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        setInputValue(event?.target.value);
    }

    return ( 
        <div className="SearchBar">
            <input 
                className='searchInput' 
                onChange={handleChange}
                placeholder="Enter address to search"
                aria-label="Enter address to search"
            />
            <button 
                className="ai-button" 
                onClick={handleSubmit}
            >
                <span className="material-icons searchIcon">search</span>
            </button>
        </div>
    );
}