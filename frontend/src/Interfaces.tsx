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
    id: string,
    lat: number,
    lon: number,
    name: string,
    address: string,
    description: string, // Specify what it is (restaraunt, car dealership, etc)
    type: string // Can be food, nature, sports, shopping, uncategorized_poi (broad category)
}