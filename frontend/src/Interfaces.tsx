export interface QueryType {
    radius: number,
    experience: Array<string>,
    activity: Array<string>,
    audience: Array<string>,
    time: Array<string>,
    season: Array<string>
}

export interface CoordinateResponse {
    data: Coordinates
}

export interface Coordinates {
    lat: string,
    lon: string
}

// TODO: Determine what a POI will contain
export interface Pois {
    id: string,
    lat: number,
    lon: number,
    tags: PoiTags,
    name: string,
    type: string,
    address: string,
    description: string
}

export interface PoiTags {
    [key: string]: string;
    amenity: string, // Check
    name: string, // Check
    cuisine: string, // Check
    takeaway: string, // Check
    wheelchair: string, // Check
    website: string, // Check
    phone: string, // Check
    address: string, // Check
    outdoor_seating: string, // Check
    opening_hours: string, // Check
    indoor_seating: string, // Check 
    drive_through: string
    shop: string, // Check
    tourism: string, // Check
    leisure: string, // Check
    craft: string, // Check
    historic: string, // Check
    email: string, // Check
    description: string, // Check
    category: string // food, nature, shopping, sports, uncategorized_poi
}

export interface PoiResponse {
    data: {element: Array<Pois>}
}
