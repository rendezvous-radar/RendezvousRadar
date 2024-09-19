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

    // Placecard information
    const [isOverview, setIsOverview] = React.useState<boolean>(true);

    // TODO: Find better way to do this
    const getFirstValidTag = (tags : PoiTags) : string | undefined => {
        if (tags.amenity) {
            return 'amenity';
        }

        if (tags.shop) {
            return 'shop'
        }
        
        if (tags.tourism) {
            return 'tourism'
        }

        if (tags.leisure) {
            return 'leisure'
        }

        if (tags.craft) {
            return 'craft'
        }

        if (tags.historic) {
            return 'historic'
        }
        return;
    };

    const capitalize = (word : string) : string => {
        if (word) {
            return word.charAt(0).toUpperCase() + word.slice(1);
        }

        else {
            return "";
        }
    }

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
                setDesc((props.poi.tags.cuisine 
                    ? capitalize(props.poi.tags.cuisine?.replace(/_/g, ' ')) + " " 
                    : ""
                ) + capitalize(props.poi.tags.amenity?.replace(/_/g, ' ')));
            } else if (validTag == "shop") {
                // Amenity is a shop
                setDesc(capitalize(props.poi.tags.shop?.replace(/_/g, ' ') + " shop"));
            } else {
                setDesc(capitalize(props.poi.tags.validTag?.replace(/_/g, ' ').toLocaleUpperCase()));
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
    
            // Add spaces around the dash in the time range
            const formattedTime = time?.replace('-', ' - ');
    
            // Expand day ranges like Mo-We to Mo, Tu, We
            const expandedDays = days.split('-').map(day => daysMap[day.trim()]);
    
            if (expandedDays.length > 1) {
                const startDay = Object.keys(daysMap).indexOf(days.split('-')[0].trim());
                const endDay = Object.keys(daysMap).indexOf(days.split('-')[1].trim());
    
                for (let i = startDay; i <= endDay; i++) {
                    result.push(`${Object.values(daysMap)[i]}: ${formattedTime}`);
                }
            } else {
                const singleDays = days.split(',').map(day => daysMap[day.trim()]);
                singleDays.forEach(day => {
                    result.push(`${day}: ${formattedTime}`);
                });
            }
        });
    
        return result;
    };

    const switchView = (state: boolean) => {
        setIsOverview(state);
        return "done";
    }

    const activeStyle = {"borderBottom": "2px solid #368DFF", "color": "#368DFF"} // Sets the style of the active window

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
                <p className="overview" style={isOverview ? activeStyle : {}} onClick={() => switchView(true)}>Overview</p>
                <p className="overview" style={isOverview ? {} : activeStyle} onClick={() => switchView(false)}>About</p>
            </div>

            {isOverview &&
                <div>
                    <p className="distance"><span className="material-icons">straighten</span>{`${Math.round(props.distance * 100) / 100}km away`}</p>
                    <p className="address"><span className="material-icons">place</span>{props.poi.tags.address}</p>
                    {props.poi.tags.opening_hours && 
                        <div className="address">
                            <span className="material-icons">schedule</span>
                            <ul className="opening-hours-list">
                                {transformHours(props.poi.tags.opening_hours).map((hour, index) => (
                                    <li key={index} className="opening-hours">{hour}</li>
                                ))}
                            </ul>
                        </div>
                    }

                    {props.poi.tags.phone && 
                        <p className="address"><span className="material-icons">phone</span>{props.poi.tags.phone}</p>
                    }
                    
                    {props.poi.tags.website && 
                        <a className="address website" href={props.poi.tags.website}><span className="material-icons">link</span>Website Link</a>
                    }

                    {props.poi.tags.email && 
                        <p className="address"><span className="material-icons">email</span>{props.poi.tags.email}</p>
                    }   
                </div>
            }

            {!isOverview &&

                <div className="about-info-grid">
                    {props.poi.tags.takeaway &&
                        <p className="about-info">Takeaway 
                            {
                                props.poi.tags.takeaway == "yes" ?
                                <span className="material-icons check">check</span> : 
                                <span className="material-icons closed">closed</span>
                            }
                        </p>
                    }

                    {props.poi.tags.wheelchair &&
                        <p className="about-info">Wheelchair 
                        {
                            props.poi.tags.wheelchair == "yes" ?
                            <span className="material-icons check">check</span> : 
                            <span className="material-icons closed">closed</span>
                        }
                    </p>
                    }

                    {props.poi.tags.drive_through &&
                        <p className="about-info">Drive Through 
                        {
                            props.poi.tags.drive_through == "yes" ?
                            <span className="material-icons check">check</span> : 
                            <span className="material-icons closed">closed</span>
                        }
                    </p>
                    }

                    {props.poi.tags.outdoor_seating &&
                        <p className="about-info">Outdoor Seating 
                        {
                            props.poi.tags.outdoor_seating == "yes" ?
                            <span className="material-icons check">check</span> : 
                            <span className="material-icons closed">closed</span>
                        }
                    </p>
                    }

                    {props.poi.tags.indoor_seating &&
                        <p className="about-info">Indoor Seating 
                        {
                            props.poi.tags.indoor_seating == "yes" ?
                            <span className="material-icons check">check</span> : 
                            <span className="material-icons closed">closed</span>
                        }
                    </p>
                    }
                </div>

            }

        </div>
    )
}