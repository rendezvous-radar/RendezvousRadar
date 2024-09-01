export interface QueryType {
    radius: string,
    experience: Array<string>,
    activity: Array<string>,
    audience: Array<string>,
    time: Array<string>,
    season: Array<string>
}

export interface Coordinates {
    lat: string,
    lon: string
}

// TODO: Determine what a POI will contain
export interface Pois {
    id: number,
    lat: number,
    lon: number,
    tags: PoiTags
}

export interface PoiTags {
    [key: string]: string;
    amenity: string, // Check
    name: string, // Check
    cuisine: string, // Check
    takeaway: string, 
    wheelchair: string,
    website: string, 
    phone: string, 
    address: string, // Check
    outdoor_seating: string,
    opening_hours: string,
    indoor_seating: string,
    drive_through: string
    shop: string, // Check
    tourism: string, // Check
    leisure: string, // Check
    craft: string, // Check
    historic: string, // Check
    email: string,
    description: string, // Check
    category: string // food, nature, shopping, sports, uncategorized_poi
}
