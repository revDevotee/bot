url = "https://docs.google.com/spreadsheets/d/1WhCpZaaugZ8WhLtbWM71Q6TrRM_oXkhD/edit?gid=963336423#gid=963336423"

# Удаляем ненужные части URL
spreadsheet_id = url.replace("https://docs.google.com/spreadsheets/d/", "").split("/")[0]

print(spreadsheet_id)

#духаст
input()
