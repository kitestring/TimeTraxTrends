import matplotlib.pyplot as plt

class XY_PlotLabeled():
	
	def createXYLabeledPlot(self, xValueLabels, xAxisLabel ,yValues, yAxisLabel, plotTitle):
	
		#xValueLabels - must be a list of strings which label each x axis value
		#xAxisLabel - string to label the x axis
		#yValues - a stirng of float values to define y axis values with the same number of values as xValueLabels
		#yAxisLabel - string to label the y axis
		#plotTitle - string to provide a title to the graph
	
		xValues = self.listComprehension(xValueLabels)
		
		plt.plot(xValues, yValues, 'co')
		# You can specify a rotation for the tick labels in degrees or with keywords.
		plt.xticks(xValues, xValueLabels, rotation='vertical')
		# Pad margins so that markers don't get clipped by the axes
		plt.margins(0.1)
		# Tweak spacing to prevent clipping of tick-labels
		plt.subplots_adjust(bottom=0.15)

		plt.ylabel(yAxisLabel)
		plt.xlabel(xAxisLabel)
		plt.title(plotTitle)
		plt.grid(True)
		plt.savefig('foo.png', bbox_inches='tight')

		plt.show()
		
	def listComprehension(self, xValues):
		enumeratedList = [i + 1 for i , item in enumerate(xValues)]
		return enumeratedList