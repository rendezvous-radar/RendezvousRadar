import React from 'react';
import FilterPanel from './FilterPanel';
import NavBar from './NavBar';

/**
 * Search Component
 *  
 * @param {Object} props - The component props.
 * @returns {JSX.Element} A React JSX element representing the Search Component, the search section of the website
*/
export default function Search(props: {}) : JSX.Element {

    // State for opening and closing the filter panel menu
    const [filterHidden, setFilterHidden] = React.useState(true);

    return ( 
        <div className='search'>
            <NavBar setFilterHidden={setFilterHidden}></NavBar>
            {filterHidden && (<FilterPanel></FilterPanel>)}
        </div>
    );
}