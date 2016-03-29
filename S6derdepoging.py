fo = open("/Users/jorisvanlammeren/Documents/Studie/Scriptie/JorisVLammeren/Data/Svalbard_S6_input.txt", "r")
print ("Name of the file: ", fo.name)
data= fo.read
print (data)
# Assuming file has following 5 lines
# This is 1st line
# This is 2nd line
# This is 3rd line
# This is 4th line
# This is 5th line



# Close opend file
fo.close()
