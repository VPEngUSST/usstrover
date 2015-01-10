import json

general_json = json.dumps([
	{'type': 'title',
	 'title': 'Rover GUI Settings'},
	{'type': 'bool',
	 'title': 'Rover Control Enable',
	 'desc': 'Do you want to drive the rover? (Test mode)',
	 'section': 'general',
	 'key': 'test_mode'},
	{'type': 'numeric',
	 'title': 'A numeric setting',
	 'desc': 'Numeric description text',
	 'section': 'general',
	 'key': 'numericexample'},
	{'type': 'title',
	'title': 'Control Settings'},
	{'type': 'options',
	 'title': 'Drive Mode',
	 'desc': 'Options description text',
	 'section': 'general',
	 'key': 'drive_mode',
	 'options': ['One Stick', 'Two Stick', 'Keyboard']},
	{'type': 'string',
	 'title': 'A string setting',
	 'desc': 'String description text',
	 'section': 'general',
	 'key': 'stringexample'},
	{'type': 'path',
	 'title': 'A path setting',
	 'desc': 'Path description text',
	 'section': 'general',
	 'key': 'pathexample'}])
	 
navigation_json = json.dumps([
	{'type': 'title',
	 'title': 'Navigation and Tracking Settings'},
	{'type': 'bool',
	 'title': 'Follow Rover',
	 'desc': 'Selects following rover current position on map screen',
	 'section': 'navigation',
	 'key': 'follow_rover'},
	 {'type': 'title',
	 'title': 'Map Settings'},
	{'type': 'numeric',
	 'title': 'Map Top Right Lattitude',
	 'desc': 'In decimal degrees',
	 'section': 'navigation',
	 'key': 'tr_lat'},
	 {'type': 'numeric',
	 'title': 'Map Top Right Longitude',
	 'desc': 'In decimal degrees',
	 'section': 'navigation',
	 'key': 'tr_lon'},
	 {'type': 'numeric',
	 'title': 'Map Bottom Left Lattitude',
	 'desc': 'In decimal degrees',
	 'section': 'navigation',
	 'key': 'bl_lat'},
	 {'type': 'numeric',
	 'title': 'Map Bottom Left Longitude',
	 'desc': 'In decimal degrees',
	 'section': 'navigation',
	 'key': 'bl_lon'},
	{'type': 'options',
	 'title': 'An options setting',
	 'desc': 'Options description text',
	 'section': 'navigation',
	 'key': 'optionsexample',
	 'options': ['option1', 'option2', 'option3']},
	{'type': 'numeric',
	 'title': 'Map Size X',
	 'desc': 'Pixels',
	 'section': 'navigation',
	 'key': 'map_size_x'},
	{'type': 'numeric',
	 'title': 'Map Size Y',
	 'desc': 'Pixels',
	 'section': 'navigation',
	 'key': 'map_size_y'},
	{'type': 'string',
	 'title': 'A string setting',
	 'desc': 'String description text',
	 'section': 'navigation',
	 'key': 'stringexample'},
	{'type': 'path',
	 'title': 'Custom Map',
	 'desc': 'Location on your hard drive',
	 'section': 'navigation',
	 'key': 'map_path'}])

  
