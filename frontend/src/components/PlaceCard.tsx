import React from 'react'
import { Pois, PoiTags } from '../Interfaces'

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

    const [desc, setDesc] = React.useState(""); // Sets description for the POI
    const [icon, setIcon] = React.useState(""); // Sets icon for the POI

    const getFirstValidTag = (tags : PoiTags) : String | undefined => {
        const tagOrder = ['amenity', 'shop', 'tourism', 'leisure', 'craft', 'historic'];
        for(const tag in tagOrder){
            if(tags.tag){
                return tag;
            }
        }
        return;
    };

    React.useEffect(() => {
        switch(props.poi.tags.category.toLowerCase()) {
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

        const validTag : String | undefined = getFirstValidTag(props.poi.tags);
        
        if(validTag){
            // If POI is amenity/restaurant
            if (validTag == "amenity") {
                setDesc((props.poi.tags.cuisine !== "" 
                    ? props.poi.tags.cuisine.replace(/_/g, ' ').toUpperCase() + " " 
                    : ""
                ) + props.poi.tags.amenity.replace(/_/g, ' ').toUpperCase());
            } else if (validTag == "shop") {
                // Amenity is a shop
                setDesc(props.poi.tags.shop.replace(/_/g, ' ').toUpperCase() + " shop");
            } else {
                setDesc(props.poi.tags.validTag?.replace(/_/g, ' ').toUpperCase());
            }
        } else {
            setDesc("");
        }
        
    }, [props.poi]);

    const handleCloseButton = () => {
        props.setHidden(true);
    }

    return (
        <div className={`app-placecard ${props.hidden ? 'invisible' : ''}`}>
            <div className="close-button"><span className="material-icons close" onClick={handleCloseButton}>close</span></div>
            <h2>{props.poi.tags.name}</h2>
            {desc && 
                <p className="placecard-desc">
                    {
                        desc
                    } 
                    {
                        icon !== "" && 
                        <span>
                            •
                            <span className="material-icons">{icon}</span>
                        </span>
                    }
                </p>
            }

            {props.poi.tags.description && 
                <p className="placecard-desc">
                    {
                        props.poi.tags.description
                    }
                </p>
            }
            <div className="choose-window">
                <p className="overview">Overview</p>
            </div>
            <p className="distance"><span className="material-icons">straighten</span>{`${Math.round(props.distance * 100) / 100}km away`}</p>
            <p className="address"><span className="material-icons">place</span>{props.poi.tags.address}</p>
        </div>
    )
}