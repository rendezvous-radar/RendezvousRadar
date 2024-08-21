import React from 'react';
import FilterPanel from './FilterPanel';
import NavBar from './NavBar';
import { QueryType } from '../Interfaces';

/**
 * Search Component
 *  
 * @param {Object} props - The component props.
 * @returns {JSX.Element} A React JSX element representing the Search Component, the search section of the website
*/
export default function Search(props: {}) : JSX.Element {

    // State for opening and closing the filter panel menu
    const [filterHidden, setFilterHidden] = React.useState(true);

    // State for the type of query
    const [query, setQuery] = React.useState<QueryType>({
        radius: "",
        experience: [],
        activity: [],
        audience: [],
        time: [],
        season: []
    })

    return ( 
        <div className='search'>
            <NavBar setFilterHidden={setFilterHidden}></NavBar>
            <FilterPanel query={query} setQuery={setQuery} className={filterHidden ? 'filter-panel-hidden' : 'filter-panel-visible'}></FilterPanel>
        </div>
    );
}