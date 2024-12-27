import React from 'react'
import { Pois, PoiTags } from '../Interfaces'

const ACTIVE_STYLE = { borderBottom: '2px solid #368DFF', color: '#368DFF' };

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

    // Placecard information
    const [isOverview, setIsOverview] = React.useState<boolean>(true);

    // Returns the first valid tag
    const getFirstValidTag = React.useCallback((tags : PoiTags) : string | undefined => {
        const keysToCheck = ['amenity', 'shop', 'tourism', 'leisure', 'craft', 'historic'];
        return keysToCheck.find(key => tags[key as keyof PoiTags]);
    }, []);

    const capitalize = (word : string) : string => { return word ? word.charAt(0).toUpperCase() + word.slice(1) : ''; }

    const getDescription = React.useCallback((): string => {
        const validTag = getFirstValidTag(props.poi.tags);

        if (!validTag) return '';

        if (validTag === 'amenity') {
            return (
                (props.poi.tags.cuisine ? capitalize(props.poi.tags.cuisine.replace(/_/g, ' ')) + ' ' : '') +
                capitalize(props.poi.tags.amenity?.replace(/_/g, ' '))
            );
        } else if (validTag === 'shop') {
            return capitalize(props.poi.tags.shop?.replace(/_/g, ' ') + ' shop');
        }
        return capitalize(props.poi.tags[validTag]?.replace(/_/g, ' ') || '');
    }, [props.poi.tags, getFirstValidTag])

    const transformHours = React.useMemo(() => {
        if (!props.poi.tags.opening_hours) return [];
        const daysMap: { [key: string]: string } = {
            "Mo": "Monday",
            "Tu": "Tuesday",
            "We": "Wednesday",
            "Th": "Thursday",
            "Fr": "Friday",
            "Sa": "Saturday",
            "Su": "Sunday"
        };
    
        const ranges = props.poi.tags.opening_hours.split(/,|;/).map((range) => range.trim());
        
        return ranges.flatMap((range) => {
            const [days, time] = range.split(' ');
            if (!days || !time) return [];
            const formattedTime = time.replace('-', ' - ');
            const dayList = days.split('-').map((day) => daysMap[day])

            if (dayList.length === 2) {
                const [start, end] = dayList.map((day) => Object.keys(daysMap).indexOf(day));
                return Object.values(daysMap).slice(start, end + 1).map((day) => `${day}: ${formattedTime}`);
            }

            return days.split(',').map((day) => `${daysMap[day]}: ${formattedTime}`);
        });
    }, [props.poi.tags.opening_hours]);

    const renderIcon = React.useMemo(() => {
        const categoryIcons : {[key: string]: string} = {
            food: 'restaurant',
            nature: 'park',
            sports: 'sports_soccer',
            shopping: 'shopping_cart',
            library: 'local_library',
            entertainment: 'attractions',
            history: 'account_balance'
        };

        return categoryIcons[props.poi.tags.category?.toLowerCase()] || '';
    }, [props.poi.tags.category]);

    const amenities = [
        { label: 'Takeaway', value: props.poi.tags.takeaway },
        { label: 'Wheelchair', value: props.poi.tags.wheelchair },
        { label: 'Drive Through', value: props.poi.tags.drive_through },
        { label: 'Outdoor Seating', value: props.poi.tags.outdoor_seating },
        { label: 'Indoor Seating', value: props.poi.tags.indoor_seating },
    ];

    const renderAmenities = () => {
        const validAmenities = amenities.filter(amenity => amenity.value);

        if (validAmenities.length === 0) {
            return <p className="about-info">No amenities available</p>;
        }

        return amenities.map(
            (amenity, index) =>
                amenity.value && (
                    <p key={index} className="about-info">
                        {amenity.label}{' '}
                        <span className="material-icons">
                            {amenity.value === 'yes' ? 'check' : 'close'}
                        </span>
                    </p>
                )
        );
    }
        

    return (
        <div className={`app-placecard ${props.hidden ? 'invisible' : ''}`}>
            <div className="close-button">
                <span className="material-icons close" onClick={() => props.setHidden(true)}>
                    close
                </span>
            </div>
            <h2>{props.poi.tags.name}</h2>
            {getDescription() && 
                <p className="placecard-desc">
                    {
                        getDescription()
                    } 
                    {
                        renderIcon !== "" && 
                        <span>
                            •
                            <span className="material-icons">{renderIcon}</span>
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
                <p className="overview" style={isOverview ? ACTIVE_STYLE : {}} onClick={() => setIsOverview(true)}>Overview</p>
                <p className="overview" style={isOverview ? {} : ACTIVE_STYLE} onClick={() => setIsOverview(false)}>About</p>
            </div>

            {isOverview ? (
                <div>
                    <p className="distance">
                        <span className="material-icons">straighten</span>
                        {`${Math.round(props.distance * 100) / 100}km away`}
                    </p>
                    <p className="address">
                        <span className="material-icons">place</span>
                        {props.poi.tags.address}
                    </p>
                    {transformHours.length > 0 && (
                        <div className="address">
                            <span className="material-icons">schedule</span>
                            <ul className="opening-hours-list">
                                {transformHours.map((hour, index) => (
                                    <li key={index} className="opening-hours">
                                        {hour}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {props.poi.tags.phone && (
                        <p className="address">
                            <span className="material-icons">phone</span>
                            {props.poi.tags.phone}
                        </p>
                    )}
                    
                    {props.poi.tags.website && (
                        <a className="address website" href={props.poi.tags.website}>
                            <span className="material-icons">link</span>Website Link
                        </a>
                    )}

                    {props.poi.tags.email && (
                        <p className="address">
                            <span className="material-icons">email</span>
                            {props.poi.tags.email}
                        </p>
                    )}   
                </div>
            ) : (
                <div className="about-info-grid">{renderAmenities()}</div>
            )}
        </div>
    )
}