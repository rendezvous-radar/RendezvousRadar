import React from 'react';
import FilterPanel from './FilterPanel';
import NavBar from './NavBar';
import { QueryType } from '../Interfaces';

/**
 * Search Component
 *  
 * @returns {JSX.Element} A React JSX element representing the Search Component, the search section of the website
*/
export default function Search() : JSX.Element {

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

    // State for user prompting a search
    const [search, setSearch] = React.useState<boolean>(false);
    
    // Where the API is called, should add loading symbol, etc
    React.useEffect(() => {
        setSearch(false);


    }, [search]);

    return ( 
        <div className='search'>
            <NavBar setFilterHidden={setFilterHidden}></NavBar>
            <FilterPanel query={query} setQuery={setQuery} setSearch={setSearch} className={filterHidden ? 'filter-panel-hidden' : 'filter-panel-visible'}></FilterPanel>
        </div>
    );
}