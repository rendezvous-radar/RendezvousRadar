import React from 'react';
import logo from '../logo.png';
import SearchBar from './SearchBar';

/**
 * NavBar Component
 *  
 * @param {Object} props - The component props.
 * @param {React.Dispatch<React.SetStateAction<boolean>>} props.setFilterHidden Sets the filterPanel component visibility
 * @param {React.Dispatch<React.SetStateAction<string>>} props.setAddress Sets the address of the API call
 * @returns {JSX.Element} A React JSX element representing the NavBar Component, the navigation bar of the website
*/
export default function NavBar(props: {
    setFilterHidden: React.Dispatch<React.SetStateAction<boolean>>, 
    setAddress: React.Dispatch<React.SetStateAction<string>>}) : JSX.Element {
    
    const handleClick = () => {
        props.setFilterHidden(prevState => !prevState);
    };

    return ( 
        <div className='app-navbar'>
            <img className="app-icon" src={logo}></img>
            <SearchBar setAddress={props.setAddress}></SearchBar>
            <span className="material-icons app-menu" onClick={handleClick}>
                menu
            </span>
        </div>
    );
}