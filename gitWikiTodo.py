import subprocess
#print subprocess.check_output("ls",stderr=subprocess.STDOUT)
def getUsername():
	username = 'Phil'
	if username == '':
		with open('gitWikiTodo.py','r') as f:
			pyString = f.read()
			u = raw_input("What's you're name?")
			out = pyString.replace("username = ''","username = '"+u+"'",1)
			f.close()
		with open('gitWikiTodo.py','w') as f:
			f.write(out)
			username = u


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
			f.close


