import { ChangeEvent } from "react";

/**
 * SearchBar Component
 *  
 * @param {Object} props - The component props.
 * @param {React.Dispatch<React.SetStateAction<string>>} props.setAddress Sets the address of the api call
 * @returns {JSX.Element} A React JSX element representing the SearchBar Component, the search bar of the website
*/
export default function SearchBar(props: {setAddress: React.Dispatch<React.SetStateAction<string>>}) : JSX.Element {

    // Sets address to current input value
    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        props.setAddress(event?.target.value);
    }

    return ( 
        <div className="SearchBar">
            <span className="material-icons searchIcon">search</span>
            <input className='searchInput' onChange={handleChange} placeholder="Vaughan, Ontario, Canada"></input>
        </div>
    );
}