import requests
import json
from typing import Generator



class AuroraCall:

	"""
	: Wrapper class to abstract calls to endpoints
	: retrieve aurora data from aurora.live api
	"""
	def __init__(self):
		self._baseURL = 'https://api.auroras.live/v1/'

	def getLocalForecast(self,lat: float,longitude: float) -> json:
		"""
		: Retrieve local forecast by latitude and longitude
		"""
		url = self._baseURL + '?type=all&lat=%s&long=%s' %(str(lat),str(longitude))
		json_url = requests.get(url)
		data = json.loads(json_url.text)
		return data

	def getArchivedData(self,utcStart: str,utcEnd: str) -> json:
		"""
		: get archived data by start and end time (string args)
		: retrieves data from one year ago
		: format: 12am
		"""
		url = self._baseURL + '?type=archive&action=search&start=%s&end=%s' %(utcStart,utcEnd)
		json_url = requests.get(url)
		data = json.loads(json_url.text)
		return data

	def getStatisticalData(self) -> json:
		"""
		: retrieve stats on archived data
		: size, start date, end date
		"""
		url = self._baseURL + '?type=archive&action=stats'
		json_url = requests.get(url)
		data = json.loads(json_url.text)
		return data

	def getAuroraLocations(self) -> json:
		"""
		: get all tracked locations from api
		"""
		url = self._baseURL + '?type=locations'
		json_url = requests.get(url)
		data = json.loads(json_url.text)
		return data

	def getGlobalForecast(self):
		"""
		: retrieve global aurora tracking locations
		: send request for local forecast by location
		: yield the result
		"""
		data = {}
		data["locations"] = []
		data["latitudes"] = []
		data["longitudes"] = []
		data["probability"] = []
		data["color"] = []
		jsonData = self.getAuroraLocations()
		for key,value in jsonData.items():
			try:
				latitude = value["lat"]
				longitude = value["long"]
				name = value["name"]
				localJsonData = self.getLocalForecast(latitude,longitude)
				data["locations"].append(name)
				data["latitudes"].append(latitude)
				data["longitudes"].append(longitude)
				data["probability"].append(localJsonData["probability"]["calculated"]["value"])
				data["color"].append(localJsonData["probability"]["calculated"]["color"])
			except:
				continue
		return json.dumps(data)
			