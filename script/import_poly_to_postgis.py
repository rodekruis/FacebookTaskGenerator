import ogr, osr
import os

database = 'facebook_mwi'
usr = 'postgres'
pw = ''

table = 'hrsl_poly2'
shp_path = '../hrsl_mwi/admin3/poly/'




def addShapefile(fn, outLayer, name):
    print('importing: ' + fn)
    
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(fn, 0)
    inLayer = inDataSource.GetLayer()

    outLayerDefn = outLayer.GetLayerDefn()

    outLayer.StartTransaction()


    # Add features to the ouput Layer
    for inFeature in inLayer:
        #print inFeature
        # Create output Feature
        outFeature = ogr.Feature(outLayerDefn)
        
        geom = inFeature.GetGeometryRef()
        outFeature.SetGeometry(geom.Clone())
        
        outFeature.SetField("admin", name)
        

        # Add field values from input Layer
        '''for i in range(0, outLayerDefn.GetFieldCount()):
            fieldDefn = outLayerDefn.GetFieldDefn(i)
            fieldName = fieldDefn.GetName()

            outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(),
                inFeature.GetField(i))
        '''
        
        # Set geometry as centroid

        outLayer.CreateFeature(outFeature)

    outFeature = None
    outLayer.CommitTransaction()


def main():
    connectionString = "PG:dbname='%s' user='%s' password='%s'" % (database, usr, pw)
    ogrds = ogr.Open(connectionString)

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)

    outLayer = ogrds.CreateLayer(table, srs, ogr.wkbPolygon, ['OVERWRITE=YES'] )
    #layerDefn = layer.GetLayerDefn()

    # add field
    admField = ogr.FieldDefn("admin3", ogr.OFTString)
    outLayer.CreateField(admField)


    counter = 1
    shpfiles = os.listdir(shp_path)
    for shp in shpfiles:
        if shp[-4:] == '.shp':
            fullfile = shp_path + shp
            print fullfile
            name = shp[:-9]
            print name, counter
            addShapefile(fullfile, outLayer, name)
            counter += 1

main()




