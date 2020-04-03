from aurora import AuroraCall
import dash
import dash_core_components as dcc
import dash_html_components as dhtml
from typing import List, Any
import plotly.express as px
import json
import pandas

STYLESHEETS = []
ac = AuroraCall()
data = pandas.read_json(ac.getGlobalForecast())

def addExternalStyleSheet(stylesheetURL: str) -> List[str]:
	"""
	: update stylesheets list with any external stylesheet URLs or local stylesheets
	"""
	STYLESHEETS.append(stylesheetURL)

def createMapBox(data: Any,lat: float,lon: float,hoverData: List[str],colorSequence: List[str],zoom: int,height: int,style: str):
	"""
	: Create plotly mapbox object
	: return object to show on page
	"""
	figure = px.scatter_mapbox(data,lat=lat,lon=lon,hover_data=hoverData,color_discrete_sequence=colorSequence,zoom=zoom,height=height)
	figure.update_layout(mapbox_style=style)
	return figure

figure = createMapBox(data,"latitudes","longitudes",["probability","color"],["fuchsia"],0,1080,"carto-darkmatter")
app = dash.Dash(__name__,external_stylesheets=STYLESHEETS)
app.layout = dhtml.Div(children=[
		dhtml.H1(children='Aurora Map'),
		dcc.Graph(id='aurora-map',
			figure=figure)
		])

if __name__ == '__main__':
	app.run_server(debug=True)


