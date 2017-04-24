

def isSaneData(data, allowedCharacters = "abcdefghijklmnopqrstuvwxyz", allowedLength = 127):
	if len(data) > allowedLength:
		return False
	for c in data:
		if c not in allowedCharacters:
			return False
	return True