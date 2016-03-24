#!
# This is statement is required by the build system to query build info

# -*-coding=utf-8 -*-
if __name__ == '__build__':
	raise Exception

import string
__date__ = string.join(string.split('$Date: 2016/3/24 23:59:00 $')[1:3], ' ')
__author__ = 'Yongkeng Fan <https://github.com/fan2fan/Python-about-OpenGL.git>'


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from Image import *
from math import *

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# Rotations for cube. 
rot = 0.0

def LoadTexture(name):
	#global texture
	image = open(name)
	
	ix = image.size[0]
	iy = image.size[1]
	image = image.tostring("raw", "RGBX", 0, -1)
	
	# Create Texture	
	id = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, id)   # 2d texture (x and y size)
	
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	#glTexImage2D(GLenum target, GLint level, GLint components, GLsizei width, GLsizei height,
	#             GLint border, GLenum format, GLenum type, const GLvoid* pixels)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	#According to the experiment: GL_LINEAR is much better than GL_NEAREST
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	
	return id

def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
	global textures, glMultiTexCoord2f, glActiveTexture, GL_TEXTURE0, GL_TEXTURE1

	print 'Checking for extension support'
	if not glMultiTexCoord2f:
		print 'No OpenGL v3.0 built-in multi-texture support, checking for extension'
		if not glMultiTexCoord2fARB:
			print 'No GL_ARB_multitexture support, sorry, cannot run this demo!'
			sys.exit(1)
		else:
			glMultiTexCoord2f = glMultiTexCoord2fARB
			glActiveTexture = glActiveTextureARB
			GL_TEXTURE0 = GL_TEXTURE0_ARB
			GL_TEXTURE1 = GL_TEXTURE1_ARB
	else:
		print 'Using OpenGL v3.0 built-in multi-texture support'
	try:
		if not glInitMultitextureARB():
			print "Help!  No GL_ARB_multitexture"
			sys.exit(1)
	except NameError, err:
		# don't need to init a built-in (or an extension any more, for that matter)
		pass
	# active the texture
	glActiveTexture(GL_TEXTURE0)
	LoadTexture('Wall.bmp')
	glEnable(GL_TEXTURE_2D)
	
	glActiveTexture(GL_TEXTURE1)
	LoadTexture('NeHe.bmp')
	glEnable(GL_TEXTURE_2D)
	
	glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND)

	glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
	glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
	glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
	glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	# glMatrixMode(GL_PROJECTION)
	# glLoadIdentity()					# Reset The Projection Matrix
										# # Calculate The Aspect Ratio Of The Window
	# gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	
	# glMatrixMode(GL_MODELVIEW)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
	if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
		Height = 1
	
	glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)

deg_rad = pi/180.0
# The main drawing function. 
def DrawGLScene():
	global rot, texture
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer
	glLoadIdentity()					# Reset The View
	glTranslatef(0.0,0.0,-5.0)			# Move Into The Screen

	glRotatef(rot,1.0,0.0,0.0)			# Rotate The Cube On It's X Axis
	glRotatef(rot,0.0,1.0,0.0)			# Rotate The Cube On It's Y Axis
	glRotatef(rot,0.0,0.0,1.0)			# Rotate The Cube On It's Z Axis
	
	# Note there does not seem to be support for this call.
	#glBindTexture(GL_TEXTURE_2D,texture)	# Rotate The Pyramid On It's Y Axis

	p = cos(rot*deg_rad)**2
	glTexEnvfv(GL_TEXTURE_ENV, GL_TEXTURE_ENV_COLOR, (p, p, p, 1))

	glBegin(GL_QUADS)			    # Start Drawing The Cube
	
	# Front Face (note that the texture's corners have to match the quad's corners)
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad
	
	# Back Face
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)	# Bottom Right Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)	# Bottom Left Of The Texture and Quad
	
	# Top Face
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)	# Bottom Left Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)	# Bottom Right Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
	
	# Bottom Face       
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)	# Top Right Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)	# Top Left Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
	
	# Right face
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)	# Bottom Right Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)	# Top Right Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)	# Top Left Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)	# Bottom Left Of The Texture and Quad
	
	# Left Face
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)	# Bottom Left Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 0.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)	# Bottom Right Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 1.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)	# Top Right Of The Texture and Quad
	glMultiTexCoord2f(GL_TEXTURE0, 0.0, 1.0); glMultiTexCoord2f(GL_TEXTURE1, 0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)	# Top Left Of The Texture and Quad
	
	glEnd();				# Done Drawing The Cube
	
	rot  = (rot + 0.2) % 360                # rotation

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
	# If escape is pressed, kill everything.
	if args[0] == ESCAPE:
		sys.exit()

def main():
	global window
	glutInit(sys.argv)

	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(640, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("Python OpenGL")

	# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.	
	glutDisplayFunc(DrawGLScene)
	
	# Uncomment this line to get full screen.
	# glutFullScreen()

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
	
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	# Register the function called when the keyboard is pressed.  
	glutKeyboardFunc(keyPressed)

	# Initialize our window. 
	InitGL(640, 480)

	# Start Event Processing Engine	
	glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
if __name__ == "__main__":
	print "Hit ESC key to quit."
	main()
