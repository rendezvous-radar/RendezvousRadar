"""
    Takes the output of the model, giving us predictions for the different categories, 
    and converts it into the actual key-value pairs used for the API.
"""

import pandas as pd
from io import StringIO

# Preds is a dictionary of the classifications
def prediction(preds):
    data = """ Activity,Key,Value,Classifications
Zipline,aerialway,zip_line,"Family-Friendly, Adventure, Outdoor, Families, Groups, Couples, Summer, Spring, Autumn"
Arts Centre,amenity,arts_centre,"Cultural, Educational, Relaxation, Entertainment, Wheelchair accessible, Indoor"
Bar,amenity,pub,"Relaxation, Dining, Sports, Indoor, Entertainment, Couples, Groups, Solo, Evening, Night"
Barbecue,amenity,bbq,"Family-Friendly, Indoor, Dining, Couples, Families, Groups, Solo, Evening, Night"
Cycle Rental,amenity,bicycle_rental,"Adventure, Family-Friendly, Romantic, Outdoor, Sports, Entertainment, Couples, Families, Groups, Solo, Summer, Spring, Autumn"
Beer garden,amenity,biergarten,"Romantic, Cultural, Relaxation, Outdoor, Dining, Couples, Groups, Solo, Afternoon, Evening, Night, Summer, Spring, Autumn"
Brothel,amenity,brothel,"Relaxation, Indoor, Entertainment, Solo, Groups, Evening, Night"
Cafe,amenity,cafe,"Romantic, Family-friendly, Relaxation, Indoor, Dining"
Casino,amenity,casino,"Relaxation, Entertainment, Indoor, Groups, Solo, Evening, Night"
Cinema,amenity,cinema,"Romantic, Family-friendly, Relaxation, Entertainment, Indoor, Couples, Families, Groups, Solo"
Community Centre,amenity,community_centre,"Family-Friendly, Adventure, Educational, Indoor, Outdoor, Sports, Entertainment, Families, Groups, Solo"
Martial Arts,amenity,dojo,"Cultural, Educational, Indoor, Sports, Groups, Solo"
Food,amenity,restaurant,"Romantic, Family-friendly, relaxation, cultural, indoor, dining"
Fitness Centre,amenity,gym,"Indoor, Sports"
Ice Cream,amenity,ice_cream,"Romantic, Family-friendly, relaxation, indoor, dining"
Karaoke,amenity,karaoke_box,"Family-friendly, relaxation, entertainment, couples, families, groups"
Library,amenity,library,"Family-friendly, relaxation, educational, indoor"
Marketplace,amenity,marketplace,"Family-friendly, cultural, outdoor, indoor, shopping"
Mosque,amenity,place_of_worship,"Cultural, educational, solo, groups, families"
Church,amenity,place_of_worship,"Cultural, educational, solo, groups, families"
Place of Worship,amenity,place_of_worship,"Cultural, educational, solo, groups, families"
Planetarium,amenity,planetarium,"Family-friendly, educational, indoor"
Pub,amenity,pub,"Relaxation, Dining, Sports, Indoor, Entertainment, Couples, Groups, Solo, Evening, Night"
Sauna,amenity,sauna,"Relaxation, Indoor"
Theatre,amenity,theatre,"Romantic, Family-friendly, relaxation, indoor, entertainment"
Mural,artwork_type,mural,"cultural, outdoor, entertainment"
Sculpture,artwork_type,sculpture,"cultural, outdoor, entertainment"
Statue,artwork_type,statue,"cultural, outdoor, entertainment"
National Park,boundary,national_park,"Romantic, family-friendly, adventure, outdoor, summer, spring, autumn"
Cathedral,building,cathedral,"Cultural, educational, solo, groups, families, couples"
Chapel,building,chapel,"Cultural, educational, solo, groups, families, couples"
Church,building,church,"Cultural, educational, solo, groups, families, couples"
Stadium,building,stadium,"Family-friendly, outdoor, sports"
Synagogue,building,synagogue,"Cultural, educational, solo, groups, families, couples"
Brewery,craft,brewery,"Cultural, educational, solo, groups, families, couples"
Distillery,craft,distillery,"Cultural, educational, solo, groups, families, couples"
Winery,craft,winery,"Cultural, educational, solo, groups, families, couples"
Path,highway,path,"Romantic, family-friendly, adventure, outdoor, summer, spring, autumn"
Track,highway,track,"family-friendly, sports, outdoor, summer, spring, autumn"
Trail,highway,trail,"Romantic, family-friendly, adventure, outdoor, summer, spring, autumn"
Archaeological Site,historic,archaeological_site,"family-friendly, adventure, outdoor, summer, spring, autumn, educational"
Battlefield,historic,battlefield,"family-friendly, adventure, outdoor, summer, spring, autumn, educational"
Historic Building,historic,building,"family-friendly, adventure, outdoor, summer, spring, autumn, educational"
Castle,historic,castle,"family-friendly, adventure, outdoor, summer, spring, autumn, educational"
Manor,historic,manor,"family-friendly, adventure, outdoor, summer, spring, autumn, educational"
Memorial,historic,memorial,"family-friendly, adventure, outdoor, summer, spring, autumn, educational"
Mine,historic,mine,"family-friendly, adventure, outdoor, summer, spring, autumn, educational"
Monument,historic,monument,"family-friendly, adventure, outdoor, summer, spring, autumn, educational"
Ruin,historic,ruins,"family-friendly, adventure, outdoor, summer, spring, autumn, educational"
Wreck,historic,wreck,"family-friendly, adventure, outdoor, summer, spring, autumn, educational"
Meadow,landuse,meadow,"family-friendly, adventure, outdoor, summer, spring, autumn, educational"
Recreation Ground,landuse,recreation_ground,"family-friendly, adventure, outdoor, summer, spring, autumn"
Reservoir,landuse,reservoir,"family-friendly, adventure, outdoor, summer, spring, autumn"
Vineyard,landuse,vineyard,"family-friendly, adventure, outdoor, summer, spring, autumn"
Beach Resort,leisure,beach_resort,"Romantic, family-friendly, outdoor, relaxation, couples, families, groups, solo, summer, spring, autumn"
Fishing Area,leisure,fishing,"family-friendly, adventure, outdoor, summer, spring, autumn"
Garden,leisure,garden,"family-friendly, adventure, outdoor, summer, spring, autumn"
Golf Course,leisure,golf_course,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Equestrian Center,leisure,horse_riding,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Ice Rink,leisure,ice_rink,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Marina,leisure,marina,"family-friendly, adventure, outdoor, summer, spring, autumn"
Miniature Golf,leisure,miniature_golf,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Nature Reserve,leisure,nature_reserve,"family-friendly, adventure, outdoor, summer, spring, autumn"
Park,leisure,park,"family-friendly, adventure, outdoor, summer, spring, autumn"
Sports Pitch,leisure,pitch,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Playground,leisure,playground,"family-friendly, adventure, outdoor, summer, spring, autumn"
Recreation Ground,leisure,recreation_ground,"family-friendly, adventure, outdoor, summer, spring, autumn"
Sports Centre,leisure,sports_centre,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Stadium,leisure,stadium,"Family-friendly, outdoor, sports"
Swimming Pool,leisure,swimming_pool,"family-friendly, indoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Running Track,leisure,track,"family-friendly, outdoor, sports, couples, families, groups, solo, summer, spring, autumn"
Water Park,leisure,water_park,"family-friendly, indoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Statue,memorial,statue,"cultural, outdoor, entertainment"
War Memorial,memorial,war_memorial,"cultural, outdoor, entertainment"
Bay,natural,bay,"family-friendly, adventure, outdoor, summer, spring, autumn"
Beach,natural,beach,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Cape,natural,cape,"family-friendly, adventure, outdoor, summer, spring, autumn"
Cave Entrance,natural,cave_entrance,"family-friendly, adventure, outdoor, summer, spring, autumn"
Cliff,natural,cliff,"family-friendly, adventure, outdoor, summer, spring, autumn"
Coastline,natural,coastline,"family-friendly, adventure, outdoor, summer, spring, autumn"
Reef,natural,reef,"family-friendly, adventure, outdoor, summer, spring, autumn"
Spring,natural,spring,"family-friendly, adventure, outdoor, summer, spring, autumn"
Valley,natural,valley,"family-friendly, adventure, outdoor, summer, spring, autumn"
Volcano,natural,volcano,"family-friendly, adventure, outdoor, summer, spring, autumn"
Island,place,island,"family-friendly, adventure, outdoor, summer, spring, autumn"
Art Shop,shop,art,"Romantic, family-friendly, cultural, shopping, indoor, couples, families, groups, solo"
Bakery,shop,bakery,"Romantic, family-friendly, cultural, shopping, indoor, couples, families, groups, solo"
Mall,shop,mall,"Romantic, family-friendly, cultural, shopping, indoor, couples, families, groups, solo"
Massage Shop,shop,massage,"Relaxation, indoor, couples, solo"
Salon,shop,salon,"Relaxation, indoor, couples, solo"
Shopping Centre,shop,shopping_centre,"family-friendly, cultural, shopping, indoor, couples, families, groups, solo"
Sports Shop,shop,sports,"family-friendly, cultural, shopping, indoor, sports, couples, families, groups, solo"
Tattoo Studio,shop,tattoo,"shopping, indoor, couples, solo"
Toy Shop,shop,toys,"family-friendly, cultural, shopping, indoor, sports, couples, families, groups, solo"
Aquarium,tourism,aquarium,"romantic, Family-friendly, adventure, relaxation, educational, indoor, couples, families, groups, solo"
Attraction,tourism,attraction,"Romantic, Family-friendly, adventure, relaxation, educational, indoor, couples, families, groups, solo"
Camp Site,tourism,camp_site,"family-friendly, adventure, outdoor, summer, spring, autumn"
Picnic Site,tourism,picnic_site,"romantic, family-friendly, adventure, outdoor, summer, spring, autumn"
Theme Park,tourism,theme_park,"romantic, family-friendly, adventure, outdoor, summer, spring, autumn"
Viewpoint,tourism,viewpoint,"romantic, family-friendly, adventure, outdoor, summer, spring, autumn"
Zoo,tourism,zoo,"romantic, Family-friendly, adventure, relaxation, educational, outdoor, couples, families, groups, solo"
Waterfall,waterway,waterfall,"romantic, family-friendly, adventure, outdoor, summer, spring, autumn"
Lighthouse,man_made,lighthouse,"romantic, family-friendly, adventure, outdoor, summer, spring, autumn" """

    df = pd.read_csv(StringIO(data))

    def activity_matches(row, preds):
        classifications = row['Classifications'].split(', ')
        return all(pred in classifications for pred in preds.values() if pred != 'Any')

    matching_activities = df[df.apply(activity_matches, axis=1, args=(preds,))]

    # Returns a key-value pair of all matching activities
    return [(row['Key'], row['Value']) for _, row in matching_activities.iterrows()]


print(prediction(preds={
    'type_of_experience': 'Family-Friendly',
    'activity_type': 'Dining',
    'target_audience': 'Families',
    'seasonality': 'Any',  
    'time_of_day': 'Any'    
    }))
