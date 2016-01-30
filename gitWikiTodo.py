import subprocess, datetime, os

def checkWiki():
	if not os.path.isdir(".git"):
		print "this doesn't seem to be a git repo"
		return None
	url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"])
	if url.find('.git') == -1:
		repo = url[url.rindex('/')+1:-1]
	else:
		repo = url[url.rindex('/')+1:url.rindex('.git')]
	wikiRepo = repo+'.wiki'
	if not os.path.isdir(wikiRepo):
		print 'wiki repo not found, git cloning ' + wikiRepo
		wikiUrl = url[:url.rindex('/')+1]+wikiRepo+'.git'
		subprocess.call(["git","clone",wikiUrl])
	else:
		print "pulling latest wiki"
		subprocess.call("( cd "+wikiRepo+" && git pull )",shell=True)
	return wikiRepo

def getUsername():
	username = subprocess.check_output(["git", "config", "user.name"])
	name = username.partition(" ")[0]
	return name

def getFile(username,wikiRepo,readwrite=0):
	fileName = wikiRepo+'/'+username+"'s-todos.md"

	try:
		with open(fileName,'r') as f:
			f.close()
	except:
		if readwrite=='read':
			print 'todo list not found'
			return 0
		elif readwrite=='write':
			subprocess.call(["touch",fileName])
			print 'todo not found, creating now'
			with open(fileName,'w') as f:
				tableHeader = 'Date | Todo\n:---: | :---'
				f.write(tableHeader)
				f.close()
		else:
			raise Error('incompatible value for readwrite in function getFile')
	return fileName

def composeTodos(fileName,todos):
	push = '\n'
	d = datetime.date.today()
	push += d.isoformat()+ ' | <ul>'
	for t in todos:
		push += '<li>'+t+'</li>'
	push += '</ul>'
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

def pushWikiChanges(wikiRepo,fileName):
	addName = fileName[fileName.rindex('/')+1:].replace(" ","\ ")
	addName = addName.replace("'","\\'")
	subprocess.call("( cd "+wikiRepo+" && git add "+addName+" )", shell = True)
	subprocess.call("( cd "+wikiRepo+" && git commit -m 'added todos' )", shell = True)
	subprocess.call("( cd "+wikiRepo+" && git push origin master )", shell = True)

def matchIdx(lists):
	taskSize = len(lists[0])
	for l in lists:
		if len(l) < taskSize:
			taskSize = len(l)
	i = 0
	while i < taskSize:
		re = []
		for l in lists:
			re.append(l[i])
		i += 1
		yield re

def readTodos(username,wikiRepo):
	fileName = getFile(username,wikiRepo,'read')
	rawList = ''
	with open(fileName,'r') as f:
		rawList = f.read()
		f.close()
	lis = []
	unlis = []
	idx = 0;
	while idx != -1:
		idx = rawList.find("<li>",idx)
		lis.append(idx)
		idx = rawList.find("</li>",idx)
		unlis.append(idx)
	lis = lis[0:-1]
	unlis = unlis[0:-1]
	todos = []
	for l, u in matchIdx([lis,unlis]):
		todos.append(rawList[l+4:u])
	return

def main():
	wikiRepo = checkWiki()
	if wikiRepo == None:
		return
	username = getUsername()
	readTodos(username,wikiRepo)
	# fileName = getFile(username,wikiRepo)
	# todos = inputTodos()
	# if todos != []:
	# 	composeTodos(fileName,todos)
	# 	pushWikiChanges(wikiRepo,fileName)

main()