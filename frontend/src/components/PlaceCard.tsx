import React from 'react'
import { Pois } from '../Interfaces'

/**
 * Placecard Component
 * @param {Object} props - The component props.
 * @param {string} props.key The id of the POI
 * @param {Pois} props.poi The selected POI
 * @param {number} props.distance The distance of the selected POI from the search origin
 * @param {boolean} props.hidden Indicates whether the component is hidden or not
 * @param {React.Dispatch<React.SetStateAction<boolean>>} props.setHidden Sets the state for hidden
 * @returns {JSX.Element} A React JSX element representing the Placecard Component, shows the information of the selected POI
*/
export default function PlaceCard(props: {
    key: string, 
    poi: Pois, 
    distance: number, 
    hidden: boolean, 
    setHidden: React.Dispatch<React.SetStateAction<boolean>>}) : JSX.Element {

    const [loading, setLoading] = React.useState(false) // Shows a loading sign while the API search is running

    const [icon, setIcon] = React.useState("") // Sets icon for the POI

    React.useEffect(() => {
        switch(props.poi.type.toLowerCase()) {
            case "food":
                setIcon("restaurant");
                break;
            case "nature":
                setIcon("park");
                break;
            case "sports":
                setIcon("sports_soccer");
                break;
            case "shopping":
                setIcon("shopping_cart");
                break;
            default:
                setIcon("");
        }
        
    }, [props.poi]);

    const handleCloseButton = () => {
        props.setHidden(true);
    }

    return (
        <div className={`app-placecard ${props.hidden ? 'invisible' : ''}`}>
            <div className="close-button"><span className="material-icons close" onClick={handleCloseButton}>close</span></div>
            <h2>{props.poi.name}</h2>
            <p className="placecard-desc">{props.poi.description} {icon !== "" && <span>•<span className="material-icons">{icon}</span></span>}</p>
            <div className="choose-window">
                <p className="overview">Overview</p>
            </div>
            <p className="distance"><span className="material-icons">straighten</span>{`${Math.round(props.distance * 100) / 100}km away`}</p>
            <p className="address"><span className="material-icons">place</span>{props.poi.address}</p>
        </div>
    )
}