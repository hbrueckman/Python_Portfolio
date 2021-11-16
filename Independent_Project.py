# This script was writtent to complete a lab from my Intro to GIS class that I orginally did all in ArcMap. I took on the challenge of completing the objective of the lab only through python script. 
# Obejecive of the lab was to complete spatial analysis through query. The lab focused on analyzing inventory data from a Forest and determining which set of forest stands meet the criteria for harvest based on certain parameters. 

# The parameters for a harvest stand to be met include: 

# 1. Owned by the University of Montana 
# 2. Must be between the ages of 70-125 years old. 
# 3. Cannot be adjacent to young stands that are between the age 1-20 years old. 
# 4. Cannot be within 250 meters of old stands that are between 150 and >200 years old. 
# 5. Cannot have monitoring plots within them 
# 6. Must have to be on land with a slope ranging from 0-15% 
# 7. Must be within 100 m of a road 
# 8. Cannot be within 20 m of a stream

# All of these parameters had to be true to determine if a forest stand was harvestable. To figure this out I systematically went through the data checking for each parameter and removing non harvest stands until I had stands that met the criteria. 

# The data I used for this included shapefiles for forest boundary, forest stands, perenial streams, and roads. I also had a forest inventory table that had information for each each stand, and I joined this table with the forest stands polygon layer. The last bit of data was XY data of points that showed where monitoring plots were. 


import geopandas as gpd





import matplotlib.pyplot as plt


# In[659]:


from shapely.geometry import Point, LineString, Polygon


# In[596]:


import shapely.speedups


# In[597]:


import numpy as np


# In[598]:





# In[599]:


bound_fp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/boundary.shp"


# In[600]:


foreststands_fp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/Forest_stands.shp"


# In[601]:


pernrf3_fp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/perennial_RF3.shp"


# In[602]:


roadclass_fp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/Road_classes.shp"


# In[603]:


forestinven_fp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/forest_inventory.dbf"


# In[604]:


forinv=gpd.read_file(forestinven_fp)


# In[605]:


forest=gpd.read_file(foreststands_fp)


# In[606]:


pern=gpd.read_file(pernrf3_fp)


# In[607]:


road=gpd.read_file(roadclass_fp)


# Checked that the coordinate systems matched in all the layers

# In[608]:


bound=gpd.read_file(bound_fp)


# In[609]:


assert_list = [bound, road, pern, forest]


# In[610]:


for a in assert_list:
    for l in assert_list:
        assert a.crs == l.crs , "CRS differs between layers"


# Determined area and made a new attribute column that displays area in acres. Since the projection is uses meters I converted it to acres by dividing it by 4,047

# In[611]:


forest['Area']=forest.area/4047


# In[612]:


forinv=forinv.drop(columns=['geometry'])


# merged the table from forest inventory that had no geospatial data with the forest stands one by linking through the column SLINK2000

# In[613]:


cutblocks=forest.merge(forinv, on='SLINK2000')


# In[614]:


cutblocksfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/cutblocks.shp"


# In[615]:


cutblocks.to_file(cutblocksfp)


# In[616]:


cutblock=gpd.read_file(cutblocksfp)


# Solidifed the join by downloading it as a new shapefile called cutblock

# Question 1: 1. How many stands are in the Cutblocks layer? What is their combined area?

# In[617]:


stand_area=cutblock['Area'].sum()
print(stand_area)


# In[618]:


stand_num=len(cutblock.index)
print(stand_num)


# Question 2: To limit all further analyses to this ownership class, open the properties window for the Cutblocks layer and build the following statement in the Query Builder on the Definition Query tab: "OWNER" = 1
# 
# Now how many stands are in the Cutblocks layer? What is their combined area?

# In[619]:


group_owner=cutblock.groupby('OWNER')


# In[620]:


group_owner.groups.keys()


# In[621]:


for key, group in group_owner:
    print('Owner:', key)
    print('number of rows:', len(group), "\n")


# one option is to group the data in table by owner and then make seperate shapefiles of these seperate owners and their rows

# In[622]:


cb_owner1=cutblock[cutblock['OWNER']==1]


# In[623]:


cb_owner1.head()


# In[624]:


print (len(cb_owner1.index))


# There are 1093 stands

# another option is to select out all the rows with owner 1 and to not go through the trouble of making a seperate shapefile. now you can find the sum of the area.

# In[625]:


print (cb_owner1['Area'].sum())


# There are 19,994 acres

# 3. How many stands are in the age group 70-125

# In[626]:


cb_70_125=cb_owner1[cb_owner1['STAND_AGE'].isin(['08', '09', '10', '11'])]


# same method of selecting out of the last selection but this time selecting multiple values in the attribute column

# In[627]:


print(len(cb_70_125.index))


# 467 trees are 70-125 in age

# 4. How many trees of the current selection are adjacent/touching trees that are in age classes 1-2? Remove the trees that are adjacent. 

# First I created a dataframe that had young trees in groups 01 and 02

# In[628]:


young_forest=cutblock[cutblock['STAND_AGE'].isin(['01','02'])]


# In[629]:


yfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/young_forest.shp"


# In[630]:


young_forest.to_file(yfp)


# In[631]:


young_forest=gpd.read_file(yfp)


# In[632]:


young_forest.plot()


# In[633]:


print(len(young_forest.index))


# In[634]:


print(len(cb_70_125.index))


# In[635]:


cb_70_125.plot()


# I also solidified my selection layer by making it a shapefile and then reading it back into python

# In[636]:


cbfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/cutblocks.shp"


# In[637]:


cb_70_125.to_file(cbfp)


# In[638]:


cb_70_125=gpd.read_file(cbfp)


# To find young trees that are adjacent to the current selection I did .touches()
# 
# This gave me a lot of trouble because .touches() functions in a way that in a 1 to 1 row wise manner. It does not check if an element of one GeoSeries touches ANY element of the other one. But it can check if each geometry of GeoSeries touches a SINGLE geometry. 
# 
# This is why a unary_union had to be applied to young_forest because it then combined all the young forest polygons to be a single geometry that cb_70_125 could run against. 

# In[639]:


adjacent=cb_70_125.touches(young_forest.unary_union)


# In[640]:


adjacent_sum=sum(adjacent)
print(adjacent_sum)


# In[641]:


cb_70_125['young_adjacent']=adjacent


# In[642]:


adj_young=cb_70_125[cb_70_125['young_adjacent']==False]


# In[643]:


adj_young


# In[644]:


adjfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/adj_young.shp"


# In[645]:


adj_young.to_file(adjfp)


# In[646]:


adj_y=gpd.read_file(adjfp)


# 4. Answer: There are now 435 trees left in the selection. 32 were removed because they were adjacent to young stands. 

# First create a layer that has only the stands in groups 13 and 14, which is the code for the trees from age 150 and older

# In[647]:


other_trees=cutblock[cutblock['STAND_AGE'].isin(['13','14'])]


# created a buffer of 250 meters from the geometries of trees that are 150 or older. I could just put in 250 without indicating units because .buffer() uses the crs dimensions, which in this case is in meters.

# In[648]:


other_trees['250_buffer']=other_trees['geometry'].buffer(250)


# In[649]:


other_trees['250_buffer'].plot()


# created a geoseriers that contains boolean values indicating if adj_y geometires intersect at all with the the other_trees buffer of 250 meters. Had to do a unary_union again so that other trees was considered one geometry to avoid problems with indexes. Also tried .within() first, but it seems that only brings back geometries that are completely within a selection.

# In[670]:


buffer=adj_y.intersects(other_trees['250_buffer'].unary_union)


# In[671]:


buffer_sum=sum(buffer)
print(buffer_sum)


# In[672]:


adj_y['250_buffer']=buffer


# In[673]:


buffer1=adj_y[adj_y['250_buffer']==False]


# In[674]:


print (buffer1['Area'].sum())


# Questions 5 and 6: 5.	This spatial query removed stands of trees from the Cut_Block layer that were aged 150 to greater than 200 years old and were within 250 meters of the current selected stands(adj_y). There are now 230 trees in the selction and their total area in acres is 4,335

# Question 7: This spatial query removes the plots that are monitoring plots. Sample_points has x and y coordinates that indicate the monitoring plots. 

# In[655]:


sample_pointfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/sample_point.dbf"
sample_point=gpd.read_file(sample_pointfp)


# In[656]:


sample_point.head()


# After reading the sample_point file in, i utilized the UTM_x and UTM_y coordinates and zipped them together to create coordinate points that function as the geometry column in the geodataframe. I chose to use the UTM coordiantes because that is the projection of the other geodataframes. 

# In[666]:


sample_point['geometry'] = [Point(xy) for xy in zip(sample_point.UTM_X, sample_point.UTM_Y)]


# In[667]:


sample_point.head()


# In[669]:


sample_point.plot()


# next I figured out which of buffer1 polygons intersected with the monitoring plots. Again I used unary_union to avoid issues with the indexes. I also found that I could do sample_point.within(buffer1.unary_union) and get the same results, but then I wasnt able to determine which of the polygons in buffer1 contained the monitoring plots, because unary_union joined the polygons to be one geometry. I also tried .contain() but this came back with 0. Im not sure what .contains does in geopandas. I assumed it was the opposite of .within(), but that didnt seem to be true. 

# In[696]:


point_contain=buffer1.intersects(sample_point.unary_union)


# In[697]:


point_sum=sum(point_contain)
print(point_sum)


# In[699]:


buffer1['sample_point']=point_contain


# In[702]:


perm_plot=buffer1[buffer1['sample_point']==False]


# In[703]:


perm_plot


# Answer Question 7: 23 stands were removed from this query based on if they are monitoring plots. This leaves 207 stands selected in Cut_Block.

# Question 8: select plots that have a slope from 0-15%

# First i grouped the perm_plot selection by SLPCLASS, and then wrote code to determine the differnt attributes for this field and realized I needed to select plots with an SLPCLASS of 0-4% and 0-5%. 

# In[704]:


group_slp=perm_plot.groupby('SLPCLASS')


# In[706]:


for key, group in group_slp:
    print('slp:', key)
    print('number of rows:', len(group), "\n")


# I made my selection of plots that had a slope of 5-15%.

# In[708]:


slope_select=perm_plot[perm_plot['SLPCLASS'].isin(['0-4%', '5-15%'])]


# In[709]:


slope_select


# Answer Question 8: There are now 70 stands selected in the Cut_Block layer selected by if they have a slope of 0-15 percent. 

# Question 9: remove any of the plots that are not within 100 meters of a road

# First I buffered the road geometry by 100 meters

# In[717]:


road_buffer_100m=road['geometry'].buffer(100)


# In[719]:


road['buffer_100m']=road_buffer_100m


# next i found which polygons of the current selection intersect with this 100 meter road buffer.  

# In[722]:


road_intersect=slope_select.intersects(road['buffer_100m'].unary_union)


# In[723]:


road_sum=sum(road_intersect)
print(road_sum)


# In[724]:


slope_select['road_buffer_100m']=road_intersect


# I selected to the polygons in which it was true that they were within 100 meters of a road

# In[727]:


road_buffer=slope_select[slope_select['road_buffer_100m']==True]


# In[728]:


road_buffer


# Answer to question 9: There are now 49 stands selected in the Cut_Block layer selected by if they are within 100 meters of a road

# Question 10: remove any plots within current selection that are within 20 meters of a stream.

# Using the same process of the other buffers, I buffered the perrenial streams by 20 meters and then figured out which of the current selection of cutblocks intersected with this buffer

# In[731]:


pern['pern_buffer']=pern['geometry'].buffer(20)


# In[732]:


stream_20m=road_buffer.intersects(pern['pern_buffer'].unary_union)


# In[733]:


stream_sum=sum(stream_20m)
print(stream_sum)


# In[734]:


road_buffer['stream_buffer_20m']=stream_20m


# In[735]:


final_Cutblocks=road_buffer[road_buffer['stream_buffer_20m']==False]


# In[736]:


final_Cutblocks


# Question 10 Answer:
# There are 33 stands left selected in the Cut_Block layer that are not within 20 meters of a stream. 
# 

# In[737]:


final_cutblocksfp="/users/haleybrueckman/desktop/computer_practice/python/Lab9_Raw_Data/final_cutblocks.shp"
final_Cutblocks.to_file(final_cutblocksfp)

# In[ ]:




