from PIL import Image, ImageChops, ImageOps
from random import shuffle
from keras.utils import np_utils

import numpy as np
import os
from ImageCutter import ImageCutter

# Load DeepLIBRAS image
def loadDeepLIBRAS():
	trainFile = os.path.join(os.path.dirname(__file__), 'DeepLIBRAS/train.txt')
	testFile = os.path.join(os.path.dirname(__file__), 'DeepLIBRAS/test.txt')

	# Image config
	original_width = 640
	original_height = 480
	cut_range = 50
	
	X_train_unsuffle = []
	Y_train_unsuffle = []
	X_train = []
	Y_train = []

	with open(trainFile) as f:
		for line in f:
			# Split the line to get file path, category and crop coords
			info = line.split('@')
			# Split the coords
			coords = info[2].split(',')

			# Read and crop the image
			img = Image.open(os.path.join(os.path.dirname(__file__), 'DeepLIBRAS/'+info[0]+'.jpg')).convert('L')
			img = ImageCutter.cut(img, {'x':int(coords[0]), 'y':int(coords[1])}, cut_range)

			# Append image to input list as a numpy array
			X_train_unsuffle.append(np.asarray(img).reshape(1, 100, 100))
			# Append category to category list
			Y_train_unsuffle.append(int(info[1]))

	index_shuf = range(len(X_train_unsuffle))
	shuffle(index_shuf)
	for i in index_shuf:
		X_train.append(X_train_unsuffle[i])
		Y_train.append(Y_train_unsuffle[i])

	X_test_unsuffle = []
	Y_test_unsuffle = []
	X_test = []
	Y_test = []

	with open(testFile) as f:
		for line in f:
			# Split the line to get file path, category and crop coords
			info = line.split('@')
			# Split the coords
			coords = info[2].split(',')

			# Read and crop the image
			img = Image.open(os.path.join(os.path.dirname(__file__), 'DeepLIBRAS/'+info[0]+'.jpg')).convert('L')
			img = ImageCutter.cut(img, {'x':int(coords[0]), 'y':int(coords[1])}, cut_range)

			# Append image to input list as a numpy array
			X_test_unsuffle.append(np.asarray(img).reshape(1, 100, 100))
			# Append category to category list
			Y_test_unsuffle.append(int(info[1]))

	index_shuf = range(len(X_test_unsuffle))
	shuffle(index_shuf)
	for i in index_shuf:
		X_test.append(X_test_unsuffle[i])
		Y_test.append(Y_test_unsuffle[i])

	# Return data
	return np.array(X_train), np.array(Y_train), np.array(X_test), np.array(Y_test)

# Load Yale Faces B image
def loadYaleFaces():
    subject = 'subject'
    actions = ['happy', 'normal', 'sad', 'surprised', 'wink']

    X_train_unsuffle = []
    Y_train_unsuffle = []
    X_test = []
    Y_test = []

    # Get train inputs
    for x in range(1,8):
        for y in range (0,5):
            img = Image.open(os.path.join(os.path.dirname(__file__), 'yalefaces/cropped/subject'+str(x).zfill(2)+'.'+actions[y])).convert('L')
            X_train_unsuffle.append(np.array(img).reshape(1, 37, 49))
            Y_train_unsuffle.append(y)

    # Get train inputs
    for x in range(9,16):
        for y in range (0,5):
            img = Image.open(os.path.join(os.path.dirname(__file__), 'yalefaces/cropped/subject'+str(x).zfill(2)+'.'+actions[y])).convert('L')
            X_test.append(np.array(img).reshape(1, 37, 49))
            Y_test.append(y)

    # Shuffle data
    X_train = []
    Y_train = []
    index_shuf = range(len(X_train_unsuffle))
    shuffle(index_shuf)
    for i in index_shuf:
        X_train.append(X_train_unsuffle[i])
        Y_train.append(Y_train_unsuffle[i])
    
    # Return data
    return np.array(X_train), np.array(Y_train), np.array(X_test), np.array(Y_test)

# Load the KDEF images
def loadKDEF():
	trainFile = os.path.join(os.path.dirname(__file__), 'KDEF/train.txt')
	testFile = os.path.join(os.path.dirname(__file__), 'KDEF/test.txt')
	nb_classes = 7

	X_train_unsuffle = []
	Y_train_unsuffle = []
	X_train = []
	Y_train = []

	# Open train info and split in lines
	with open(trainFile) as f:
		for line in f:
			# split file info
			info = line.split('@')

			# Read the image
			img = Image.open(os.path.join(os.path.dirname(__file__), 'KDEF/'+info[0])).convert('L')
			img = makeThumb(img)
			# Append image to input list as a numpy array
			X_train_unsuffle.append(np.asarray(img).reshape(1, 100, 100))

			# Append category to category list
			Y_train_unsuffle.append(int(info[1]))

	# suffle train data
	index_shuf = range(len(X_train_unsuffle))
	shuffle(index_shuf)
	for i in index_shuf:
		X_train.append(X_train_unsuffle[i])
		Y_train.append(Y_train_unsuffle[i])

	X_test_unsuffle = []
	Y_test_unsuffle = []
	X_test = []
	Y_test = []

	# Open test info and split in lines
	with open(testFile) as f:
		for line in f:
			# split file info
			info = line.split('@')

			# Read the image
			img = Image.open('datasets/KDEF/'+info[0]).convert('L')
			img = makeThumb(img)
			# Append image to input list as a numpy array
			X_test_unsuffle.append(np.asarray(img).reshape(1, 100, 100))

			# Append category to category list
			Y_test_unsuffle.append(int(info[1]))

	# suffle test data
	index_shuf = range(len(X_test_unsuffle))
	shuffle(index_shuf)
	for i in index_shuf:
		X_test.append(X_test_unsuffle[i])
		Y_test.append(Y_test_unsuffle[i])

	# Convert class to categorical
	Y_train = np_utils.to_categorical(np.array(Y_train), nb_classes)
	Y_test = np_utils.to_categorical(np.array(Y_test), nb_classes)

	# Return data
	return np.array(X_train), Y_train, np.array(X_test), Y_test, nb_classes

def loadKDEFinRGB():
	trainFile = os.path.join(os.path.dirname(__file__), 'KDEF/train.txt')
	testFile = os.path.join(os.path.dirname(__file__), 'KDEF/test.txt')
	nb_classes = 7

	X_train_unsuffle = []
	Y_train_unsuffle = []
	X_train = []
	Y_train = []

	# Open train info and split in lines
	with open(trainFile) as f:
		for line in f:
			# split file info
			info = line.split('@')

			# Read the image
			img = Image.open(os.path.join(os.path.dirname(__file__), 'KDEF/'+info[0]))
			img = makeThumb(img)
			# Append image to input list as a numpy array
			X_train_unsuffle.append(np.asarray(img).reshape(3, 100, 100))

			# Append category to category list
			Y_train_unsuffle.append(int(info[1]))

	# suffle train data
	index_shuf = range(len(X_train_unsuffle))
	shuffle(index_shuf)
	for i in index_shuf:
		X_train.append(X_train_unsuffle[i])
		Y_train.append(Y_train_unsuffle[i])

	X_test_unsuffle = []
	Y_test_unsuffle = []
	X_test = []
	Y_test = []

	# Open test info and split in lines
	with open(testFile) as f:
		for line in f:
			# split file info
			info = line.split('@')

			# Read the image
			img = Image.open('datasets/KDEF/'+info[0])
			img = makeThumb(img)
			# Append image to input list as a numpy array
			X_test_unsuffle.append(np.asarray(img).reshape(3, 100, 100)) # FORMATO (CANAIS, ALTURA, LARGURA)

			# Append category to category list
			Y_test_unsuffle.append(int(info[1]))

	# suffle test data
	index_shuf = range(len(X_test_unsuffle))
	shuffle(index_shuf)
	for i in index_shuf:
		X_test.append(X_test_unsuffle[i])
		Y_test.append(Y_test_unsuffle[i])

	# Convert class to categorical
	Y_train = np_utils.to_categorical(np.array(Y_train), nb_classes)
	Y_test = np_utils.to_categorical(np.array(Y_test), nb_classes)

	# Return data
	return np.array(X_train), Y_train, np.array(X_test), Y_test, nb_classes

# Load the CK+ Dataset
def loadTrainAndTest(basePath, nb_classes):
	trainFile = os.path.join(os.path.dirname(__file__), basePath+'/train.txt')
	testFile = os.path.join(os.path.dirname(__file__), basePath+'/test.txt')

	trainLine = None
	with open(trainFile) as f:
		trainLine = f.read().splitlines()

	testLine = None
	with open(testFile) as f:
		testLine = f.read().splitlines()

	# Read the data
	X_train, Y_train = read(trainLine, basePath)
	X_test, Y_test   = read(testLine, basePath)

	# Convert class to categorical
	Y_train = np_utils.to_categorical(np.array(Y_train), nb_classes)
	Y_test = np_utils.to_categorical(np.array(Y_test), nb_classes)
	
	# Return data
	return np.array(X_train), Y_train, np.array(X_test), Y_test, nb_classes

'''
Load any database in folds
k         = The numbers of folds
i         = The fold iteration
basePath  = The database base path(DeepLIBRAS, KDEF, CK+)
nb_classe = The number of classes in database
'''
def loadBatchs(k, iteration, basePath, nb_classes):
	# Get and read the info file
	info = os.path.join(os.path.dirname(__file__), basePath+'/info.txt')
	lines = None
	with open(info) as f:
		lines = f.read().splitlines()
		
	# Calculate the folds
	elByBatch = len(lines) / k
	start = elByBatch * iteration
	end = start + elByBatch
	
	# Split the info in the folds
	test = lines[start:end]
	train = lines[0:start] + lines[end:len(lines)]

	# Read the data
	X_train, Y_train = read(train, basePath)
	X_test, Y_test   = read(test, basePath)

	# Convert class to categorical
	Y_train = np_utils.to_categorical(np.array(Y_train), nb_classes)
	Y_test = np_utils.to_categorical(np.array(Y_test), nb_classes)
	
	# Return data
	return np.array(X_train).astype('float32'), Y_train, np.array(X_test).astype('float32'), Y_test, nb_classes

'''
Read all images from a list in a specific path
Suffle the read data
fileList = The file list
basePath = The path
'''
def read(fileList, basePath):
	X_data_unsuffle = []
	Y_data_unsuffle = []
	X_data = []
	Y_data = []

	for line in fileList:
		# split file info
		info = line.split('@')

		# Read the image
		img = Image.open(os.path.join(os.path.dirname(__file__), basePath+'/'+info[0])).convert('L')
		
		if(basePath == 'DeepLIBRAS'):
			# Split the coords
			coords = info[2].split(',')
			img = ImageCutter.cut(img, {'x':int(coords[0]), 'y':int(coords[1])}, 50)
		else:
			img = makeThumb(img)
		
		# Append image to input list as a numpy array
		X_data_unsuffle.append(np.asarray(img).reshape(1, 100, 100)) # FORMATO (CANAIS, ALTURA, LARGURA)

		# Append category to category list
		Y_data_unsuffle.append(int(info[1]))

	# suffle data
	index_shuf = range(len(X_data_unsuffle))
	shuffle(index_shuf)
	for i in index_shuf:
		X_data.append(X_data_unsuffle[i])
		Y_data.append(Y_data_unsuffle[i])

	return X_data, Y_data

'''
Transform a image to 100x100 size
from: http://stackoverflow.com/a/9103783
'''
def makeThumb(image, size=(100,100), pad=False):
    image.thumbnail(size, Image.ANTIALIAS)
    image_size = image.size

    if pad:
        thumb = image.crop( (0, 0, size[0], size[1]) )

        offset_x = max( (size[0] - image_size[0]) / 2, 0 )
        offset_y = max( (size[1] - image_size[1]) / 2, 0 )

        thumb = ImageChops.offset(thumb, offset_x, offset_y)

    else:
        thumb = ImageOps.fit(image, size, Image.ANTIALIAS, (0.5, 0.5))

    return thumb
