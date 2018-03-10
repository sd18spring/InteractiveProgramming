import geoplotlib
thedata = geoplotlib.utils.read_csv('testcsv.csv')
#geoplotlib.hist(thedata['lat'],thedata['lon'],thedata['GDP'], cmap='hot', alpha=220, colorscale='sqrt', binsize=16, show_tooltip=False, scalemin=0, scalemax=None, f_group=None)
geoplotlib.show()
