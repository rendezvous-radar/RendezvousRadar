/**
 * SearchBar Component
 *  
 * @returns {JSX.Element} A React JSX element representing the SearchBar Component, the search bar of the website
*/
export default function SearchBar() : JSX.Element {
    return ( 
        <div className="SearchBar">
            <span className="material-icons searchIcon">search</span>
            <input className='searchInput'></input>
        </div>
    );
}