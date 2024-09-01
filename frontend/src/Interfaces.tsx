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
    amenity: string,
    name: string,
    cuisine: string,
    takeaway: string,
    wheelchair: string,
    website: string,
    phone: string,
    address: string,
    outdoor_seating: string,
    opening_hours: string,
    indoor_seating: string,
    drive_through: string
    shop: string,
    tourism: string,
    leisure: string,
    office: string,
    craft: string,
    historic: string,
    email: string,
    description: string,
    category: string // food, nature, shopping, sports, uncategorized_poi
}
