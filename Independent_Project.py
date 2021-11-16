
# This script was writtent to complete a lab from my Intro to GIS class that I orginally did all in ArcMap.
# I took on the challenge of completing the objective of the lab only through python script. 
# The Obejecive of the lab was to complete spatial analysis through query. 
# The lab focused on analyzing inventory data from a Forest and determining which set of forest stands meet the criteria for harvest based on certain parameters.
# In this script I include questions from the lab that I answer.

# The parameters for a harvest stand to be met include: 

# 1. Owned by the University of Montana 
# 2. Must be between the ages of 70-125 years old. 
# 3. Cannot be adjacent to young stands that are between the age 1-20 years old. 
# 4. Cannot be within 250 meters of old stands that are between 150 and >200 years old. 
# 5. Cannot have monitoring plots within them 
# 6. Must have to be on land with a slope ranging from 0-15% 
# 7. Must be within 100 m of a road 
# 8. Cannot be within 20 m of a stream

# All of these parameters had to be true to determine if a forest stand was harvestable. 
# To figure this out I systematically went through the data checking for each parameter and removed non harvest stands until I had stands that met the criteria. 

# The data I used for this included:
# -Shape files of forest boundary, forest stands, perenial streams, and roads. 
# -Forest inventory table that had information for each each stand, which I then joined with the forest stands polygon layer. 
# -XY data of points that showed where monitoring plots were. 




import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon
import shapely.speedups
import numpy as np

# I made file paths for each shapefile

bound_fp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/boundary.shp"
foreststands_fp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/Forest_stands.shp"
pernrf3_fp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/perennial_RF3.shp"
roadclass_fp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/Road_classes.shp"
forestinven_fp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/forest_inventory.dbf"

# Read each file using geopandas and checked that the coordinate systems matched. 

forinv=gpd.read_file(forestinven_fp)
forest=gpd.read_file(foreststands_fp)
pern=gpd.read_file(pernrf3_fp)
road=gpd.read_file(roadclass_fp)
bound=gpd.read_file(bound_fp)


assert_list = [bound, road, pern, forest]

for a in assert_list:
    for l in assert_list:
        assert a.crs == l.crs , "CRS differs between layers"

# The coodrinate systems matched among the layers.        

# Determined area and made a new attribute column that displays area in acres. Since the projection uses meters I converted it to acres by dividing it by 4,047

forest['Area']=forest.area/4047
forinv=forinv.drop(columns=['geometry'])

# Merged the table from forest inventory that had no geospatial data with the forest stands polygon layer by joining them through the column SLINK2000.

cutblocks=forest.merge(forinv, on='SLINK2000')

# Solidifed the join by downloading it as a new shapefile called cutblock

cutblocksfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/cutblocks.shp"
cutblocks.to_file(cutblocksfp)
cutblock=gpd.read_file(cutblocksfp)



# Question 1: How many stands are in the Cutblocks layer? What is their combined area?

stand_area=cutblock['Area'].sum()
print(stand_area)

stand_num=len(cutblock.index)
print(stand_num)

# Answer: 1,998 stands in cutblock layer with an area of 43,607.75 acres. 



# Question 2: How many stands are owned by University? What is their combined area?

# The forest inventory code for stands owned by UMT is "OWNER" = 1

# one option to solve this is to group the data in table by owner and then make seperate shapefiles of these seperate owners and their rows.

group_owner=cutblock.groupby('OWNER')
group_owner.groups.keys()
for key, group in group_owner:
    print('Owner:', key)
    print('number of rows:', len(group), "\n")
       
# another option to solve this is to select out all the rows with owner 1 and to not go through the trouble of making a seperate shapefile. Now you can find the sum of the area.

cb_owner1=cutblock[cutblock['OWNER']==1]
print (len(cb_owner1.index))
print (cb_owner1['Area'].sum())

#  Answer: There are 1,093 stands owned by Univeristy of Montana and they make up an area of 19,994 acres. 



# Question 3: How many stands are in the age group 70-125?

# same method of selecting out of the last selection but this time selecting multiple values in the attribute column
cb_70_125=cb_owner1[cb_owner1['STAND_AGE'].isin(['08', '09', '10', '11'])]

# I solidified my selection layer by making it a shapefile and then reading it back into python so it was permanent. 

cbfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/cutblocks.shp"
cb_70_125.to_file(cbfp)
cb_70_125=gpd.read_file(cbfp)

print(len(cb_70_125.index))

# Answer: 467 stands are 70-125 in age



# 4. How many trees of the current selection (cb_70_125) are adjacent to stands that are in 1-20 years old (groups 1 and 2)? Remove the stands that are adjacent. 

# First I created a dataframe that had young trees in groups 01 and 02

young_forest=cutblock[cutblock['STAND_AGE'].isin(['01','02'])]

# Made the selection permanent by reading it into a shapefile.

yfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/young_forest.shp"
young_forest.to_file(yfp)
young_forest=gpd.read_file(yfp)

# To find young trees that are adjacent to the current selection I ran .touches() function through geopandas. 
# This gave me a lot of trouble because .touches() functions in a 1 to 1 row wise manner. It does not check if an element of one GeoSeries touches ANY element of the other one. But it can check if each geometry of GeoSeries touches a SINGLE geometry. 
# I ended up running geopandas unary_union function and then doing .touches(). Unary_union combined all the young forest polygons to be a single geometry that cb_70_125 could then run against to see if it touched the young stands.

adjacent=cb_70_125.touches(young_forest.unary_union)

adjacent_sum=sum(adjacent)
print(adjacent_sum)

# There are 32 stands in the current selection that are adjacent to young stands. Now these must be removed so we are left with stands not adjacent to young stands.

# I made a column in my current selection of cb_70_125 that had boolean values for whether or not each polygon stand was adjacent to a young stand. 

cb_70_125['young_adjacent']=adjacent

# I made a new selection of all the stands that had a boolean value of false, which meant they were not adjacent. 

adj_young=cb_70_125[cb_70_125['young_adjacent']==False]

# I then made the new selection permanent. 

adjfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/adj_young.shp"
adj_young.to_file(adjfp)
adj_y=gpd.read_file(adjfp)


# Answer to #4: There are now 435 trees left in the selection. 32 were removed because they were adjacent to young stands. 



# Question 5: Figure out how many stands are within 250 meters of old stands between the ages of 150 to greater than 200 years old. Remove these stands from the selection.

# First I created a layer that has only the stands in groups 13 and 14, which is the code for the trees from age 150 and older

other_trees=cutblock[cutblock['STAND_AGE'].isin(['13','14'])]


# I created a buffer of 250 meters from the geometries of trees that are 150 or older. 
# I put 250 in the code without indicating units because .buffer() uses the crs dimensions, which in this case is in meters.

other_trees['250_buffer']=other_trees['geometry'].buffer(250)
other_trees['250_buffer'].plot()


# I then created a geoseriers that contains boolean values indicating if adj_y geometires intersect at all with the the other_trees buffer of 250 meters. 
# This included doing a unary_union again so that other trees was considered one geometry to avoid problems with indexes. Also tried .within() first, but it seems that only solves for geometries that are completely within a selection.

buffer=adj_y.intersects(other_trees['250_buffer'].unary_union)

buffer_sum=sum(buffer)
print(buffer_sum)

adj_y['250_buffer']=buffer

buffer1=adj_y[adj_y['250_buffer']==False]

print (buffer1['Area'].sum())


# Answer 5: There are now 230 trees now in the selction and their total area in acres is 4,335



# Question 6: Remove the stands that have a monitoring plot within them from the selection. How many stands are are now in the selection?

# I used a table called Sample_points that had x and y coordinates indicating the monitoring plots. 

sample_pointfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/sample_point.dbf"
sample_point=gpd.read_file(sample_pointfp)

# After reading the sample_point file in, i utilized the columns called UTM_x and UTM_y coordinates and zipped them together to create coordinate points that now function as the geometry column in the geodataframe. 
# I chose to use the UTM coordiantes because that is the projection of the other geodataframes. 

sample_point['geometry'] = [Point(xy) for xy in zip(sample_point.UTM_X, sample_point.UTM_Y)]

sample_point.plot()

# next I figured out which of the selection (buffer1) polygons intersected with the monitoring plots. 
# Again I used unary_union to avoid issues with the indexes and then used .intersects() 
# I also found that I could do sample_point.within(buffer1.unary_union) and get the same results, but then I wasnt able to determine which of the polygons in buffer1 contained the monitoring plots, because unary_union joined the polygons to be one geometry. 
# I also tried .contain() but this came back with 0. Im not sure what .contains does in geopandas. I assumed it was the opposite of .within(), but that didnt seem to be true. 

point_contain=buffer1.intersects(sample_point.unary_union)

point_sum=sum(point_contain)
print(point_sum)

buffer1['sample_point']=point_contain

perm_plot=buffer1[buffer1['sample_point']==False]


# Answer: 23 stands were removed from this query based on if they are monitoring plots. This leaves 207 stands selected in the harvest Cut_Block.



# Question 7: select only the plots that have a slope from 0-15%. How many stands are now in the selectoin?

# First I grouped the current selection (perm_plot) by SLPCLASS, and then wrote code to determine the differnt attributes for this field and realized I needed to select plots with an SLPCLASS of 0-4% and 5-15%. 

group_slp=perm_plot.groupby('SLPCLASS')

for key, group in group_slp:
    print('slp:', key)
    print('number of rows:', len(group), "\n")


# I made my selection of plots that had a slope of 0-15%.

slope_select=perm_plot[perm_plot['SLPCLASS'].isin(['0-4%', '5-15%'])]

# Answer: There are now 70 stands selected in the Cut_Block layer selected by if they have a slope of 0-15 percent. 



# Question 8: Remove any of the plots that are not within 100 meters of a road. How many stands are now in the selection?

# First I buffered the road geometry by 100 meters

road_buffer_100m=road['geometry'].buffer(100)

road['buffer_100m']=road_buffer_100m


# Next i found which polygons of the current selection intersect with this 100 meter road buffer.  

road_intersect=slope_select.intersects(road['buffer_100m'].unary_union)


road_sum=sum(road_intersect)
print(road_sum)

slope_select['road_buffer_100m']=road_intersect


# I selected to the polygons which had the boolean value of true, meaning they were within 100 meters of a road

road_buffer=slope_select[slope_select['road_buffer_100m']==True]


road_buffer


# Answer: There are now 49 stands selected in the Cut_Block layer selected by if they are within 100 meters of a road



# Question 9: Remove any plots within the current selection (road_buffer) that are within 20 meters of a stream.

# Using the same process of the other buffers, I buffered the perrenial streams by 20 meters and then figured out which of the current selection of cutblocks intersected with this buffer

pern['pern_buffer']=pern['geometry'].buffer(20)

stream_20m=road_buffer.intersects(pern['pern_buffer'].unary_union)

stream_sum=sum(stream_20m)
print(stream_sum)

road_buffer['stream_buffer_20m']=stream_20m

final_Cutblocks=road_buffer[road_buffer['stream_buffer_20m']==False]

final_Cutblocks

# Answer: There are 33 stands left selected in the Cut_Block layer that are not within 20 meters of a stream. 

final_Cutblocks.plot()
print(len(final_Cutblocks.index))

# Final Answer: After going through each parameter and removing the appropiate non harvest stands, there ended up being 33 stands that fit the criteria for harvest. 

# To finish I saved final_cutblocks to be a permanent shapefile on my computer. 

final_cutblocksfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/final_cutblocks.shp"
final_Cutblocks.to_file(final_cutblocksfp)
