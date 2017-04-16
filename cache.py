import pickle

vpath = 'static/Cloud/4'
c = {}

CACHE_SIZE = 16

s1 = 'string 1'
s2 = 'string 2'
s3 = 'string 3'
s4 = 'string 4'


r1 = 'result 1'
r2 = 'result 2'
r3 = 'result 3'
r4 = 'result 4'

# cache = {s1:[r1,1],s2:[r2,0],s3:[r3,2],s4:[r4,8]}
cache = {}

def getresult(cache,sq):
    if(cache.get(sq,None)==None):
        return None
    else:
        print "\nCache[sq] - ",type(cache[sq][0])
        return cache[sq][0]

def loadCache(filepath):
	with open(filepath, 'rb') as input:
	    cache = pickle.load(input)
	return cache

def saveCache(cache, filepath):
    with open(filepath, 'wb') as output:
        pickle.dump(cache, output, pickle.HIGHEST_PROTOCOL)

def update(cache,s1,r1):
	if(cache.get(s1,None)==None):
		if(len(cache)<CACHE_SIZE):
			print 'cache not full, new element'
			cache[s1] = [r1,0]
		else:
			print 'cache full, new element'
			Max = 0
			ind = ''
			for item in cache:
				if(cache[item][1]>Max):
					Max = cache[item][1]
					ind = item
			del cache[ind]
			cache[s1] = [r1,0]
	else:
		print 'old element'
		cache[s1][1]=0

	for item in cache:
		cache[item][1]+=1
	return cache

print '\n----------------------'
update(cache,s1,r1)
print cache

print '\n----------------------'
update(cache,s2,r2)
print cache

print '\n----------------------'
update(cache,s3,r3)
print cache

print '\n----------------------'
update(cache,s1,r1)
print cache

print '\n----------------------'
update(cache,s2,r2)
print cache

print '\n----------------------'
update(cache,s4,r4)
print cache

''' Log Out'''
saveCache(cache,vpath+'/cache.pickle')
cache = {}
print '\nCCR : ',cache

''' Log In'''
cache = loadCache(vpath+'/cache.pickle')
print '\nLC : ',cache

''' Check in Cache'''
answer = getresult(cache,s4)
print '\nAnswer : ',answer
