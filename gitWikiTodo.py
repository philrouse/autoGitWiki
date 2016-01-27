import subprocess
#print subprocess.check_output("ls",stderr=subprocess.STDOUT)
def getUsername():
	username = subprocess.check_output(["git", "config", "user.name"])
	name = username.partition(" ")[0]
	return name

def getFile(username):
	fileName = 'autoGitWiki.wiki/'+username+"'s todos.md"

	try:
		with open(fileName,'r') as f:
			return f
	except:
		subprocess.call(["touch",fileName])
		print 'todo not found, creating now'
		with open(fileName,'w') as f:
			tableHeader = 'Date | Todo\n:---: | :---'
			f.write(tableHeader)
			f.close()
	return fileName

def main():
	username = getUsername()
	fileName = getFile(username)
	print username

main()
