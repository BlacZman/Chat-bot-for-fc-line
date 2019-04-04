def Decender(de):
	Checker = 0
	decoded = ""
	decoder = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','!','@','#','$','%','^','&','*','(',')','-','_','=','+','[',
   		'{',']','}','\\','|',';',':','\'','"',',','<','.','>','/','?',' ','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4',
    	'5','6','7','8','9')
	changer = 0
	multi = 1
	decodething = de
	lengthDecoder = len(decoder)
	lengthDecodething = len(decodething)
	rand = decodething[lengthDecodething-4:lengthDecodething+1]
	rand = int(rand, 16)
	for x in range(lengthDecodething-5):
		for y in range(lengthDecoder):
			if (y - x - changer + (93 * multi)) > (rand % 93):
				multi = 0
			while (y - x - changer + (93*multi)) < (rand % 93):
				multi += 1
			if decoder[y] == decodething[x]:
				decoded += decoder[(y - x - changer + (93 * multi)) - (rand % 93)]
				changer = (changer + 1) % 10
				Checker = 1
			if Checker == 1:
				break
		Checker = 0
	return decoded