import json
import re

from bs4 import BeautifulSoup


def get_gpa_sat_act():
	current_title = ""
	current_tuple = [None, None, None, None, None]
	json_strings = '['
	for i in range(0, 146):
		file = open(f"data/{i}", "r")
		json_data = json.loads(file.read())
		current_title = json_data["title"].replace("http://www.prepscholar.com/sat/s/colleges/", "").replace(
			"-admission-requirements", "")
		html_data = BeautifulSoup(json_data["content"], "lxml")

		# Get the Averages
		for h2 in html_data.find_all("h2", text=True):
			string_gpa = h2.text
			if "Average GPA" in string_gpa:
				actual_numerical_value = float(string_gpa.split(':')[1])
				if actual_numerical_value is None: pass
				current_tuple[0] = actual_numerical_value
			elif "Average SAT:" in string_gpa:
				actual_numerical_value = int(string_gpa.split(':')[1].split('(')[0])
				if actual_numerical_value is None: pass
				current_tuple[1] = actual_numerical_value
			elif "Average ACT:" in string_gpa:
				actual_numerical_value = int(string_gpa.split(':')[1])
				if actual_numerical_value is None: pass
				current_tuple[4] = actual_numerical_value

		new_sat_table = html_data.find_all("table")[0]
		try:
			averages_row = new_sat_table.find_all("tr")[4]
		except IndexError:
			print(f"INDEX ERROR AT {new_sat_table}")
			averages_row = new_sat_table.find_all("tr")[3]
		print(averages_row.find_all("td")[2].text)
		# current_tuple[3] = int(averages_row.find_all("td")[2].text)
		try:
			current_tuple[2] = int(averages_row.find_all("td")[2].text)
		except ValueError:
			print("SKIPPING UNIVERSITY AT {}".format(current_tuple[0]))
			continue

		try:
			current_tuple[3] = int(averages_row.find_all("td")[3].text)

		except ValueError:
			print("SKIPPING UNIVERSITY AT {}".format(current_tuple[0]))
			continue

		if i == 145:
			cur_string = '''
						{{
							"model": "Matcher.University",
							"pk": {}, 
							"fields": {{
								"name": "{}",
								"average_gpa": {}, 
								"average_sat_score": {}, 
								"sat_percentile_25": {},
								"sat_percentile_75": {},
								"average_act_score": {}
							}}
						}}
						'''.format(i, current_title.replace(" ", "_"), current_tuple[0], current_tuple[1],
			                       current_tuple[2], current_tuple[3], current_tuple[4])
			cur_string = re.sub('\s+', '', cur_string)
			json_strings += cur_string

		else:
			cur_string = '''
			{{
				"model": "Matcher.University",
				"pk": {}, 
				"fields": {{
					"name": "{}",
					"average_gpa": {}, 
					"average_sat_score": {}, 
					"sat_percentile_25": {},
					"sat_percentile_75": {},
					"average_act_score": {}
				}}
			}},
			'''.format(i, current_title.replace(" ", "_"), current_tuple[0], current_tuple[1],
			           current_tuple[2], current_tuple[3], current_tuple[4])
			cur_string = re.sub('\s+', '', cur_string)
			json_strings += cur_string

	json_strings += "]"
	return json_strings


parse_data = get_gpa_sat_act()
print(parse_data)
json_data = json.loads(parse_data)
with open("./university_dump.json", 'w') as jd:
	json.dump(json_data, jd)
