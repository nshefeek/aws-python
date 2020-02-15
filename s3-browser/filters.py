import os
import mimetypes
import arrow

def parse_datetime(date_str):
	dt = arrow.get(date_str)
	return dt.humanize()

def get_filetype(filename):
	file_info = os.path.splitext(filename)
	ext = file_info[1]

	try:
		return mimetypes.types_map[ext]
	except KeyError:
		return 'Unknown'