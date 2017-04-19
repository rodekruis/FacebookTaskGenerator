
'''
gdalwarp \
-q \
-cutline /home/raymond/terglobo/projecten/rodekruis/facebook/test_polygons_wgs84.shp \
-csql "select * from test_polygons_wgs84 where name='gebied1' or name='gebied2'" \
-tr 0.00027777778 0.00027777778 \
-crop_to_cutline \
-of GTiff \
-overwrite \
/home/raymond/terglobo/projecten/rodekruis/facebook/hrsl_mwi_part.tif \
/home/raymond/terglobo/projecten/rodekruis/facebook/hrsl_mwi/hrsl_mwi_clip.tif
'''


'''
gdal_polygonize.py \ 
/home/raymond/terglobo/projecten/rodekruis/facebook/hrsl_mwi/admin3/AFRMWI10301.tif \
-f "ESRI Shapefile" 
/home/raymond/terglobo/projecten/rodekruis/facebook/hrsl_mwi/admin3/AFRMWI10301_poly AFRMWI10301_poly
'''

#real file
#/home/raymond/terglobo/projecten/rodekruis/facebook/hrsl_mwi/hrsl_mwi.tif





from osgeo import ogr
import time
#from subprocess import call
import os



def create_gdalwarp_command(name, base_name, field_name):
    result = 'gdalwarp '
    result += '-q '
    result += '-cutline ' + admin_areas + ' '
    result += '-csql "select * from ' + base_name + ' where ' + field_name + '=\'' + name + '\'" '
    result += '-tr 0.00027777778 0.00027777778 '
    result += '-crop_to_cutline '
    result += '-of GTiff '
    result += '-overwrite '
    result += hrsl_raster + ' '
    result += raster_dir + name + '.tif'
    return result

def create_gdal_polygonize_command(base_name):
    result = 'python /usr/bin/gdal_polygonize.py '
    result += raster_dir + base_name + '.tif '
    result += '-f "ESRI Shapefile" '
    result += poly_dir + base_name + '_poly.shp ' + base_name
    return result



'''
# fake data
#admin_areas = '/home/raymond/terglobo/projecten/rodekruis/facebook/'
#admin_areas_basename = 'test_polygons_wgs84'
#field_name = 'name'
#hrsl_raster = '/home/raymond/terglobo/projecten/rodekruis/facebook/hrsl_mwi_part.tif'
'''

# real data (malawi)
admin_areas_path = '/home/raymond/terglobo/projecten/rodekruis/facebook/hrsl_mwi/mwi_popa_adm3_tradauth_geonode_nso2008_ocha/'
admin_areas_basename = 'mwi_popa_adm3_tradauth_geonode_nso2008_ocha'
field_name = 'P_CODE'
hrsl_raster = '/home/raymond/terglobo/projecten/rodekruis/facebook/hrsl_mwi/hrsl_mwi.tif'

# working dirs
hrsl_output_dir = '/home/raymond/terglobo/projecten/rodekruis/facebook/hrsl_mwi/admin3/'
raster_dir = hrsl_output_dir + 'raster/'
poly_dir = hrsl_output_dir + 'poly/'

t00 = time.time()

#open input datasource
admin_areas = admin_areas_path + admin_areas_basename + '.shp'
in_driver = ogr.GetDriverByName('ESRI Shapefile')
admin_data = in_driver.Open(admin_areas, 0)

if admin_data is None:
    print 'Could not open %s' % (admin_areas)

admin_layer = admin_data.GetLayer()
feature_count = admin_layer.GetFeatureCount()
print feature_count

counter = 1

for feature in admin_layer:
    t0 = time.time()
    #print feature
    name = feature.GetField(field_name)
    print '--- ' + name + ' (' + str(counter) + ') ---'

    cmd = create_gdalwarp_command(name, admin_areas_basename, field_name)
    print cmd
    os.system(cmd)

    cmd = create_gdal_polygonize_command(name)
    print cmd
    os.system(cmd)

    print('area time: ' + str(round(time.time() - t0, 3)) + ' seconds')
    #break # quit after first feature (for dev puposes)
    counter += 1

print('total time: ' + str(round(time.time() - t00, 3)) + ' seconds')

