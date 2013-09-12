import sys, getopt

argv = sys.argv[:]


#for a in argv:
#    print (a) 

try:
    opts, args = getopt.getopt(argv[1:],"hi:o:",["ifile=","ofile="])
except getopt.GetoptError:
    print 'error'
    sys.exit(2)

for opt, arg in opts:
    print (opt + ' :: ' + arg) 

print ('fing')

