from healpy import cartview,read_map
from pickle import dump 
from numpy import linspace, meshgrid
from matplotlib.pyplot import close
fl=-1

class MapSlicer(object):
    """
    Map Slicer object: instantiate with a healpix map and use methods to convert units and produce cuts from desired map regions.
    """
    def __init__(self, map_to_cut):
        if isinstance(map_to_cut,str):
            self.map = read_map(map_to_cut,field=fl)
        else:
            self.map = map_to_cut
        
    def map_val(self, theta, phi):
        """
        Returns the value of the map at a given theta and phi in degrees.
        """
        return get_interp_val(self.map,theta,phi)
    
    def cut_map(self, rot, res=900, out_put_file = None):
        """
        Returns map cut from desired region from the given longitudinal and latitudinal ranges (assuming small engough for flat 
        sky limit)"
        """
        map_cut=cartview(self.map, rot=rot,lonra=[-10,10],latra=[-5,5],xsize=res,ysize=res,return_projected_map=True)
        close()
        return map_cut
    
        if out_put_file != None:
            dump(map_cut,open(out_put_file,'wb'), protocol = -1)
    