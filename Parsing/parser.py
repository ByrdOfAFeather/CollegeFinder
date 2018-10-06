import json

from bs4 import BeautifulSoup

lister = []
for i in range(0, 146):
	file = open(f"data/{i}", "r")
	json_data = json.loads(file.read())
	html_data = BeautifulSoup(json_data["content"], "lxml")
	print(html_data)
	all_titles = html_data.find_all("td")
	print(all_titles)
	for h2 in html_data.find_all("h2"):
		string_gpa = str(h2).replace("<h2>", "").replace("</h2>", "")
		if "Average GPA" in string_gpa:
			# print(h2)
			lister.append(string_gpa)
		elif "Average SAT:" in string_gpa:
			# print(h2)
			lister.append(string_gpa)
		elif "Average ACT:" in string_gpa:
			# print(h2)
			lister.append(string_gpa)

print(lister)
