


invalid_characters = ['<','>','&','%','"',"'"]

def valid_content(content):
	for invalid_character in invalid_characters:
		if invalid_character in content:
			return "There is an invalid character in your comment"
		else:
			return content

print valid_content("hello")