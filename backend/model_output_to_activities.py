"""
    Takes the output of the model, giving us predictions for the different categories, 
    and converts it into the actual key-value pairs used for the API.
"""

import pandas as pd
from io import StringIO

# Preds is a dictionary of the classifications
def prediction(preds):
    data = """Activity,Key,Value,Classifications
Zipline,aerialway,zip_line,"Family-Friendly, Adventure, Outdoor, Sports, Families, Groups, Couples, Solo, Summer, Spring, Autumn, Morning, Afternoon, Evening, Night"
Arts Centre,amenity,arts_centre,"Cultural, Educational, Relaxation, Entertainment, Wheelchair accessible, Indoor, Families, Groups, Couples, Solo, Summer, Spring, Autumn, Winter, Morning, Afternoon, Evening, Night"
Bar,amenity,pub,"Relaxation, Dining, Sports, Indoor, Entertainment, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Barbecue,amenity,bbq,"Family-Friendly, Indoor, Dining, Couples, Families, Groups, Solo, Evening, Night, Afternoon, Summer, Spring, Winter, Autumn"
Cycle Rental,amenity,bicycle_rental,"Adventure, Family-Friendly, Romantic, Outdoor, Sports, Entertainment, Couples, Families, Groups, Solo, Summer, Spring, Autumn"
Beer garden,amenity,biergarten,"Romantic, Cultural, Relaxation, Outdoor, Dining, Couples, Groups, Solo, Afternoon, Evening, Night, Summer, Spring, Autumn"
Brothel,amenity,brothel,"Relaxation, Indoor, Entertainment, Solo, Groups, Evening, Night"
Cafe,amenity,cafe,"Romantic, Family-friendly, Relaxation, Indoor, Dining, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Casino,amenity,casino,"Relaxation, Entertainment, Indoor, Groups, Solo, Evening, Couples, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Cinema,amenity,cinema,"Romantic, Family-friendly, Relaxation, Entertainment, Indoor, Couples, Families, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Community Centre,amenity,community_centre,"Family-Friendly, Adventure, Educational, Indoor, Outdoor, Sports, Entertainment, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Martial Arts,amenity,dojo,"Cultural, Educational, Indoor, Sports, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Food,amenity,restaurant,"Romantic, Family-friendly, relaxation, cultural, indoor, dining, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Fitness Centre,amenity,gym,"Indoor, Sports, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Ice Cream,amenity,ice_cream,"Romantic, Family-friendly, relaxation, indoor, dining, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Karaoke,amenity,karaoke_box,"Family-friendly, relaxation, entertainment, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Library,amenity,library,"Family-friendly, relaxation, educational, indoor, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Marketplace,amenity,marketplace,"Family-friendly, cultural, outdoor, indoor, shopping, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Mosque,amenity,place_of_worship,"Cultural, educational, solo, groups, families, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Church,amenity,place_of_worship,"Cultural, educational, solo, groups, families, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Place of Worship,amenity,place_of_worship,"Cultural, educational, solo, groups, families, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Planetarium,amenity,planetarium,"Family-friendly, educational, indoor, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Pub,amenity,pub,"Relaxation, Dining, Sports, Indoor, Entertainment, Couples, Groups, Solo, Evening, Night, Summer, Winter, Spring, Autumn"
Sauna,amenity,sauna,"Relaxation, Indoor, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Theatre,amenity,theatre,"Romantic, Family-friendly, relaxation, indoor, entertainment, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Mural,artwork_type,mural,"cultural, outdoor, entertainment, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Sculpture,artwork_type,sculpture,"cultural, outdoor, entertainment, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Statue,artwork_type,statue,"cultural, outdoor, entertainment, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
National Park,boundary,national_park,"Romantic, family-friendly, adventure, outdoor, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Cathedral,building,cathedral,"Cultural, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Chapel,building,chapel,"Cultural, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Church,building,church,"Cultural, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Stadium,building,stadium,"Family-friendly, outdoor, sports, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Synagogue,building,synagogue,"Cultural, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Brewery,craft,brewery,"Cultural, educational, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Distillery,craft,distillery,"Cultural, educational, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Winery,craft,winery,"Cultural, educational, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Path,highway,path,"Romantic, family-friendly, adventure, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer,, Spring, Autumn"
Track,highway,track,"family-friendly, sports, outdoor, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Trail,highway,trail,"Romantic, family-friendly, adventure, outdoor, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Archaeological Site,historic,archaeological_site,"family-friendly, adventure, outdoor, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Battlefield,historic,battlefield,"family-friendly, adventure, outdoor, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Historic Building,historic,building,"family-friendly, adventure, outdoor, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Castle,historic,castle,"family-friendly, adventure, outdoor, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Manor,historic,manor,"family-friendly, adventure, outdoor, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Memorial,historic,memorial,"family-friendly, adventure, outdoor, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Mine,historic,mine,"family-friendly, adventure, outdoor, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Monument,historic,monument,"family-friendly, adventure, outdoor, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Ruin,historic,ruins,"family-friendly, adventure, outdoor, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Wreck,historic,wreck,"family-friendly, adventure, outdoor, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Meadow,landuse,meadow,"family-friendly, adventure, outdoor, educational, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Recreation Ground,landuse,recreation_ground,"family-friendly, adventure, outdoor, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Reservoir,landuse,reservoir,"family-friendly, adventure, outdoor, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Vineyard,landuse,vineyard,"family-friendly, adventure, outdoor, Families, Couples, Groups, Solo, Evening, Night, Afternoon, Morning, Summer, Winter, Spring, Autumn"
Beach Resort,leisure,beach_resort,"Romantic, family-friendly, outdoor, relaxation, couples, families, groups, solo, summer, spring, autumn"
Fishing Area,leisure,fishing,"family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Garden,leisure,garden,"family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Golf Course,leisure,golf_course,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Equestrian Center,leisure,horse_riding,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Ice Rink,leisure,ice_rink,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Marina,leisure,marina,"family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Miniature Golf,leisure,miniature_golf,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Nature Reserve,leisure,nature_reserve,"family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Park,leisure,park,"family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Sports Pitch,leisure,pitch,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Playground,leisure,playground,"family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Recreation Ground,leisure,recreation_ground,"family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Sports Centre,leisure,sports_centre,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Stadium,leisure,stadium,"Family-friendly, outdoor, sports, summer, spring, autumn, couples, families, groups, solo"
Swimming Pool,leisure,swimming_pool,"family-friendly, indoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Running Track,leisure,track,"family-friendly, outdoor, sports, couples, families, groups, solo, summer, spring, autumn"
Water Park,leisure,water_park,"family-friendly, indoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Statue,memorial,statue,"cultural, outdoor, entertainment, couples, families, groups, solo, summer, spring, autumn, winter"
War Memorial,memorial,war_memorial,"cultural, outdoor, entertainment, couples, families, groups, solo, summer, spring, autumn, winter"
Bay,natural,bay,"family-friendly, adventure, outdoor, summer, spring, autumn, families, groups, solo, couples"
Beach,natural,beach,"family-friendly, outdoor, relaxation, sports, couples, families, groups, solo, summer, spring, autumn"
Cape,natural,cape,"family-friendly, adventure, outdoor, summer, spring, autumn, families, groups, solo, couples"
Cave Entrance,natural,cave_entrance,"family-friendly, adventure, outdoor, summer, spring, autumn, families, groups, solo, couples"
Cliff,natural,cliff,"family-friendly, adventure, outdoor, summer, spring, autumn, families, groups, solo, couples"
Coastline,natural,coastline,"family-friendly, adventure, outdoor, summer, spring, autumn, families, groups, solo, couples"
Reef,natural,reef,"family-friendly, adventure, outdoor, summer, spring, autumn, families, groups, solo, couples"
Spring,natural,spring,"family-friendly, adventure, outdoor, summer, spring, autumn, families, groups, solo, couples"
Valley,natural,valley,"family-friendly, adventure, outdoor, summer, spring, autumn, families, groups, solo, couples"
Volcano,natural,volcano,"family-friendly, adventure, outdoor, summer, spring, autumn, families, groups, solo, couples"
Island,place,island,"family-friendly, adventure, outdoor, summer, spring, autumn, families, groups, solo, couples"
Art Shop,shop,art,"Romantic, family-friendly, cultural, shopping, indoor, couples, families, groups, solo, summer, spring, autumn, winter"
Bakery,shop,bakery,"Romantic, family-friendly, cultural, shopping, indoor, couples, families, groups, solo, summer, spring, autumn, winter"
Mall,shop,mall,"Romantic, family-friendly, cultural, shopping, indoor, couples, families, groups, solo, summer, spring, autumn, winter"
Massage Shop,shop,massage,"Relaxation, indoor, couples, solo, groups, summer, spring, autumn, winter"
Salon,shop,salon,"Relaxation, indoor, couples, solo, groups, summer, spring, autumn, winter"
Shopping Centre,shop,shopping_centre,"family-friendly, cultural, shopping, indoor, couples, families, groups, solo, summer, spring, autumn, winter"
Sports Shop,shop,sports,"family-friendly, cultural, shopping, indoor, sports, couples, families, groups, solo, summer, spring, autumn, winter"
Tattoo Studio,shop,tattoo,"shopping, indoor, couples, solo, groups, summer, spring, autumn, winter"
Toy Shop,shop,toys,"family-friendly, cultural, shopping, indoor, sports, couples, families, groups, solo, summer, spring, autumn, winter"
Aquarium,tourism,aquarium,"romantic, Family-friendly, adventure, relaxation, educational, indoor, couples, families, groups, solo, summer, spring, autumn, winter"
Attraction,tourism,attraction,"Romantic, Family-friendly, adventure, relaxation, educational, indoor, couples, families, groups, solo, summer, spring, autumn, winter"
Camp Site,tourism,camp_site,"family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Picnic Site,tourism,picnic_site,"romantic, family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Theme Park,tourism,theme_park,"romantic, family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Viewpoint,tourism,viewpoint,"romantic, family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Zoo,tourism,zoo,"romantic, Family-friendly, adventure, relaxation, educational, outdoor, couples, families, groups, solo"
Waterfall,waterway,waterfall,"romantic, family-friendly, adventure, outdoor, summer, spring, autumn, couples, families, groups, solo"
Lighthouse,man_made,lighthouse,"romantic, family-friendly, adventure, outdoor, summer, spring, autumn, winter, couples, families, groups, solo" """

    df = pd.read_csv(StringIO(data))

    def activity_matches(row, preds):
        classifications = set(row['Classifications'].lower().split(', '))
        return all(any(pred.lower() in classifications or pred == 'Any' for pred in pred_list) for pred_list in preds.values())

    matching_activities = df[df.apply(activity_matches, axis=1, args=(preds,))]

    return [(row['Key'], row['Value']) for _, row in matching_activities.iterrows()]

# The preds should now be a dictionary where each key is a category and the value is a list of strings
print(prediction(preds={
    'type_of_experience': ['Family-Friendly', 'Adventure'],
    'activity_type': ['Dining', 'Outdoor'],
    'target_audience': ['Families', 'Groups'],
    'seasonality': ['Summer', 'Autumn', 'Any'],  
    'time_of_day': ['Morning', 'Afternoon', 'Any']
}))