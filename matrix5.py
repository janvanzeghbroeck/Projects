# cd desktop/pythonfun
# python matrix5.py
# clear - clears terminal

import os
import random
import time
import Tkinter 
from Tkinter import *
import tkMessageBox

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# now, to clear the screen
cls()


#Functions
#----------------------------------------------------------

#finds the world you are looking for
def w(num):
	together = ['world',str(num)]
	return worlds[''.join(together)] #returns the world or choice as a variable

#function for creating holes
def holes(row):
	w(row)
	dice = [1,1,2,2,2,3,3,4]
	n_holes = dice[random.randint(0,len(dice)-1)] #num walls = random of dice
	for j in range(1,n_holes):
		hole_loc = random.randint(0,world_size-1)#randomizes the location
		w(row)[hole_loc] = 'X' # sets a hole as 'X'

#function for creating a monster
def mon(row):
	dice = [0,1,1,1,2] #only spawns one mon - need for loop as in holes
	num_mon = dice[random.randint(0,len(dice)-1)]
	if num_mon>0:
		mon_loc = random.randint(0,world_size-1)
		row[mon_loc] = 'M'

#function for creating coins
def coin(row):
	num_coin = random.randint(0,1)
	if num_coin>0:
		coin_loc = random.randint(0,world_size-1)
		row[coin_loc] = 'O'
		
#function for creating daggers
def dagger(row):
	dice = [0,0,0,0,0,0,0,1]
	num_dagger = dice[random.randint(0,len(dice)-1)]
	if num_dagger>0:
		dagger_loc = random.randint(0,world_size-1)
		row[dagger_loc] = '|'
		
#function for moving monsters
#def move_mon(row):Jan

#function for find
def find(array,x):
	loc = []
	for i in range(0,len(array)):
		if array[i] ==x:
			loc.append(i)	
	if loc ==[]:
		return len(array)#returns the length of the array if nothing is found
	else:
		return loc #returns an array of the locations of x in array

#window controls
#----------------------------------------------------------
window = Tkinter.Tk()
def isleft():
	print 'left <<<'
def isup():
	print 'up ^^^'
def isdown():
	print 'down vvv'
def isright():
	print 'right >>>'


up = Tkinter.Button(window, text = '^', command = isup)
left = Tkinter.Button(window, text = '<', command = isleft)
right = Tkinter.Button(window, text = '>', command = isright)
down = Tkinter.Button(window, text = 'v', command = isdown)



#Creating variables for the worlds etc
#----------------------------------------------------------

world_size = 9 #num of squares in each world
coins_to_win = 20 #maybe set it up as an infinite game with high scores

#creates the blank worlds
world1 = [' ']*world_size
world2 = [' ']*world_size
world3 = [' ']*world_size
world4 = [' ']*world_size

#sets the worlds up in a dict
worlds = {'world1': world1, 
	'world2': world2, 
	'world3': world3,
	'world4': world4
}

num_worlds = len(worlds)


#set the player and other start numbers 
global p_start, p_loc, coin_count

p_start = random.randint(0,world_size-1)
p_loc = p_start
p_world = 2 #what world the player is in
mon_world = 0 #what world the monster is in
coin_count = 0
dagger_count = 1
rows_created = num_worlds


dead = 0 #to check if a player is dead: dead = 0 is not dead

# creates holes in worlds
for i in range(1,num_worlds+1):
	holes(i)

print 'You (P) are in a dungeon with monsters (M), try to collect as many coins (0) as possible'
print 'Daggers (|) can kill monsters you run into but you can only carry two at a time'
print 'You have 5 min'
print ' '

#starts game loop
#----------------------------------------------------------


start_time =time.time()
end_time = start_time + 5*60


while time.time() < end_time:#coin_count < coins_to_win: #
		#prints world1 and world2 with player position and walls

	if dead == 1:
		print 'You DIED by falling down a hole'
		print 'You ended with %d coins' % coin_count
		print 'You travels through %d rows' % rows_created
		break
	elif dead ==2:
		print 'You got KILLED by a monster'
		print 'You ended with %d coins' % coin_count
		print 'You travels through %d rows' % rows_created
		break
		
	w(p_world)[p_start] = 'P' #sets the player in the world
	
	#limits the dagger number to 2 daggers
	if dagger_count >2:
		dagger_count = 2
	
	print 'Coins = %d' %coin_count
	print 'Daggers = %d' %dagger_count
	right_now = time.time()
	print 'Time remaining (min):'
	print (end_time-right_now)/60
	
	#prints worlds
	for i in range(1,num_worlds+1):
		print '%r \n' % w(i) 
	
	#move input ----------
	move = raw_input('please move (up = w, left = a, down = s, right = d >')
	
	
	#moving left and right
	if move!='s' and move!='w': #could use move =='a' or move == 'd'
		if move == 'a' and p_start!=0:
			d = -1
		elif move == 'd' and p_start!=world_size-1:
			d = 1
			
		if w(p_world)[p_loc+d] == 'O': #checks if collecting a coin
			coin_count = coin_count+1
			p_loc = p_start + d
		elif w(p_world)[p_loc+d]=='|': #checks if collecting a dagger
			dagger_count = dagger_count+1
			p_loc = p_start + d
		elif w(p_world)[p_loc+d] == 'X': #checks if you move into a wall and die
			dead =1
		elif w(p_world)[p_loc+d] == 'M': #checks if you move into a monster and die
			if dagger_count>0:
				dagger_count = dagger_count-1
			else:
				dead =2
		else:
			p_loc = p_start+d 
		d=0
	
	#moving up
	if move == 'w' and p_world != 1:
		if w(p_world-1)[p_loc] == 'O': #checks if collecting a coin
			coin_count = coin_count+1
		elif w(p_world-1)[p_loc] == '|': #checks if collecting a dagger
			dagger_count = dagger_count+1
		elif w(p_world-1)[p_loc] == 'X': #checks if you move into a wall and die
			dead =1
		elif w(p_world-1)[p_loc] == 'M': #checks if you move into a monster and die
			if dagger_count>0:
				dagger_count = dagger_count-1
			else:
				dead =2
		
		p_world = p_world-1
		w(p_world+1)[p_loc] = ' '
		
	
	#moving down
	#w(p_world+1) = the world ahead of the player world
	if move == 's':
		if w(p_world+1)[p_loc] == 'O': #checks if collecting a coin
			coin_count = coin_count+1
		elif w(p_world+1)[p_loc] == '|': #checks if collecting a dagger
			dagger_count = dagger_count+1
		elif w(p_world+1)[p_loc] == 'X': #checks if you move into a wall and die
			dead =1
		elif w(p_world+1)[p_loc] == 'M': #checks if you move into a monster and die
			if dagger_count>0:
				dagger_count = dagger_count-1
			else:
				dead =2
		if p_world ==2:
			worlds['world1'] = worlds['world2']
			w(1)[p_loc] = ' '
			worlds['world2'] = worlds['world3']
			worlds['world3'] = worlds['world4']
			worlds['world4'] = [' ']*world_size
			
			
			#create new wall,coins, and monsters for last world
			dagger(w(len(worlds)))
			coin(w(len(worlds)))
			holes(len(worlds))
			mon(w(len(worlds)))#havent changed to input just world num
			
			rows_created = rows_created+1
			
		elif p_world == 1:
			p_world = p_world+1
			w(p_world-1)[p_loc] = ' '
# end moving ------------
		
	#saves the new location of the player and blanks the old one		
	w(p_world)[p_start] = ' '
	w(p_world)[p_loc] = 'P'	
		
		
	#moves the monster in worlds
	for i in range (1,num_worlds+1): #what world are we on
		mon_loc = find(w(i),'M') #find mon_loc is an array of locations
		if mon_loc == world_size: #if true there is no monster
			print
		else:
			for j in range (0,len(mon_loc)): #what monster we are on
			#if statement for mon AI to move towards player 
				if mon_loc[j] < p_start:
					mon_dice = [1,1,2,2,2,3] #1=left (lower) 2 = right (higher)
				elif mon_loc[j] > p_start:
					mon_dice = [1,1,1,2,2,3]
				else:
					mon_dice = [1,1,2,2,3]
				rand_move = random.randint(0,len(mon_dice)-1)
				mon_move = mon_dice[rand_move]
			#prevents move if there is no monster or if the player moves down
				#move left
				if mon_move == 1 and mon_loc[j]!=0 and w(i)[mon_loc[j]-1]!='X' and w(i)[mon_loc[j]-1]!='M':
					w(i)[mon_loc[j]] = ' '
					mon_loc[j] = mon_loc[j]-1
					w(i)[mon_loc[j]] = 'M'
					mon_world = i
				#move right
				# if monster move is 2 (right) and mon is not on the end and to the right is not a hole or a mon
				elif mon_move == 2 and mon_loc[j]!=world_size-1 and w(i)[mon_loc[j]+1]!='X' and w(i)[mon_loc[j]+1]!='M':
					w(i)[mon_loc[j]] = ' '
					mon_loc[j]= mon_loc[j]+1
					w(i)[mon_loc[j]] = 'M'
					mon_world = i
				#move down a world (up the screen)
				elif mon_move == 3 and i!=1 and w(i-1)[mon_loc[j]]!='X' and w(i-1)[mon_loc[j]]!='M':
					w(i-1)[mon_loc[j]] = 'M'
					w(i)[mon_loc[j]] = ' '
					mon_world = i-1
				#move up a world (down the screen) - not in use right now
				#NEED: way to check which monsters moved and not let them move again
				elif mon_move == 4 and i!=num_worlds and w(i+1)[mon_loc[j]]!='X' and w(i+1)[mon_loc[j]]!='M':
					w(i+1)[mon_loc[j]] = 'M'
					w(i)[mon_loc[j]] = ' '
					mon_world = i+1

				
				if	mon_world == p_world and mon_loc[j] == p_loc:
					if dagger_count >0:
						dagger_count = dagger_count-1
					elif dagger_count ==0:
						dead = 2



#super monsters
	
	#resets the player start location as the player location and clears the terminal
	p_start = p_loc
	cls()
	
	
#end game loop	
#----------------------------------------------------------



#checks that the player is not dead and won the game	
if dead ==0:
	print 'You ran out of time and got %d coins!' %coin_count
	print 'Sorry, your Princess is in another castle...'
	print 'You travels through %d rows' % rows_created
	
	
	
	
#Highscore board
#----------------------------------------------------------
#checks for a high score and then adds it to the high score board
read_scores = open('scores.txt','r')
scores = read_scores.readlines()
read_names = open('names.txt','r')
names = read_names.readlines()


#creates integer file for scores
int_scores = []
for i in range (0,len(names)):
	int_scores.append(int(scores[i]))
	
	
lowest = min(int_scores)
low_loc = find(int_scores, min(int_scores))

if coin_count > lowest:
	name = raw_input('You got a high score! Input your name: ')
	scores[low_loc[0]] = '%s\n' %str(coin_count)
	names[low_loc[0]] = '%s\n' %name


#NEEDS: sort scores (and names) from highest to lowest

# rewrites the textfiles
read_scores.close()
read_names.close()
	
open('scores.txt','w').close()
open('names.txt','w').close()

append_scores = open('scores.txt','a')
append_names = open('names.txt','a')

for i in range (0,len(scores)):
	append_scores.write(scores[i])
	append_names.write(names[i])
	
append_scores.close()
append_names.close()
	
	
# prints the score board
high_scores = []
for i in range (0,len(names)):
	high_scores.append('%s = %s' %(names[i],scores[i]))
	
print 'High Score Board:' 
for i in range (0,len(high_scores)):
	print high_scores[i]





