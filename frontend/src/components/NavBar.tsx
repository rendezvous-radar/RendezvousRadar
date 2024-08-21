import React from 'react';
import logo from '../logo.png';
import SearchBar from './SearchBar';

/**
 * NavBar Component
 *  
 * @param {Object} props - The component props.
 * @returns {JSX.Element} A React JSX element representing the NavBar Component, the navigation bar of the website
*/
export default function NavBar(props: {setFilterHidden: React.Dispatch<React.SetStateAction<boolean>>}) : JSX.Element {
    
    const handleClick = () => {
        props.setFilterHidden(prevState => !prevState);
    };

    return ( 
        <div className='app-navbar'>
            <img className="app-icon" src={logo}></img>
            <SearchBar></SearchBar>
            <div className='app-options'>
                <button>Address</button>
                <button>Search</button>
            </div>
            <span className="material-icons app-menu" onClick={handleClick}>
                menu
            </span>
        </div>
    );
}