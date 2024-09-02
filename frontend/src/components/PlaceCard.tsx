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

    const getFirstValidTag = (tags : PoiTags) : string | undefined => {
        const tagOrder = ['amenity', 'shop', 'tourism', 'leisure', 'craft', 'historic'];
        for(const tag in tagOrder){
            if(tags[tag]){
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

        const validTag : string | undefined = getFirstValidTag(props.poi.tags);
        
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

    const transformHours = (string: string) => {
        const daysMap: { [key: string]: string } = {
            "Mo": "Monday",
            "Tu": "Tuesday",
            "We": "Wednesday",
            "Th": "Thursday",
            "Fr": "Friday",
            "Sa": "Saturday",
            "Su": "Sunday"
        };
    
        const ranges = string.split(/,|;/);
        const result = [] as Array<string>;
    
        ranges.forEach(range => {
            // Extract the days and time range
            const [days, time] = range.trim().split(' ');
            
            // Expand day ranges like Mo-We to Mo, Tu, We
            const expandedDays = days.split('-').map(day => daysMap[day.trim()]);
    
            if (expandedDays.length > 1) {
                const startDay = Object.keys(daysMap).indexOf(days.split('-')[0].trim());
                const endDay = Object.keys(daysMap).indexOf(days.split('-')[1].trim());
    
                for (let i = startDay; i <= endDay; i++) {
                    result.push(`${Object.values(daysMap)[i]}: ${time}`);
                }
            } else {
                const singleDays = days.split(',').map(day => daysMap[day.trim()]);
                singleDays.forEach(day => {
                    result.push(`${day}: ${time}`);
                });
            }
        });
    
        return result;
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
                <p className="overview">About</p>
            </div>
            <p className="distance"><span className="material-icons">straighten</span>{`${Math.round(props.distance * 100) / 100}km away`}</p>
            <p className="address"><span className="material-icons">place</span>{props.poi.tags.address}</p>
            {props.poi.tags.opening_hours && 
                <p className="address"><span className="material-icons">schedule</span>{transformHours(props.poi.tags.opening_hours)}</p>
            }

            {props.poi.tags.phone && 
                <p className="address"><span className="material-icons">phone</span>{props.poi.tags.phone}</p>
            }
            
            {props.poi.tags.website && 
                <p className="address"><span className="material-icons">link</span>{props.poi.tags.website}</p>
            }

            {props.poi.tags.email && 
                <p className="address"><span className="material-icons">email</span>{props.poi.tags.email}</p>
            }   

        </div>
    )
}