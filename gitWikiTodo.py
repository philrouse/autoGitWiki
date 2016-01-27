import subprocess, datetime

#print subprocess.check_output("ls",stderr=subprocess.STDOUT)
def getUsername():
	username = subprocess.check_output(["git", "config", "user.name"])
	name = username.partition(" ")[0]
	return name

def getFile(username):
	fileName = 'autoGitWiki.wiki/'+username+"'s todos.md"

	try:
		with open(fileName,'r') as f:
			f.close()
	except:
		subprocess.call(["touch",fileName])
		print 'todo not found, creating now'
		with open(fileName,'w') as f:
			tableHeader = 'Date | Todo\n:---: | :---'
			f.write(tableHeader)
			f.close()
	return fileName

def composeTodos(fileName,todos):
	push = '\n'
	d = datetime.date.today()
	push += d.isoformat()+ ' | <ul>'
	for t in todos:
		push += '<li>'+t+'</li>'
	push += '</ul>'
	print fileName
	with open(fileName,'a') as f:
		f.write(push)
		f.close()

def inputTodos():
	todos = []
	done = False
	t = raw_input('Enter your todos:\n')
	while t != '':
		todos.append(t)
		t = raw_input('')
	return todos


def main():
	username = getUsername()
	fileName = getFile(username)
	todos = inputTodos()
	if todos != []:
		composeTodos(fileName,todos)

main()