#!/usr/bin/env python

import os
import glfw
import OpenGL.GL as gl
import OpenGL.GLU as glu
import PIL.Image as Image
import random

window_width = 640
window_height = 480

twinkle = False
tp = False
num = 50

class Star(object):
    def __init__(self):
        r, g, b = (0, 0, 0)
        dist = 0
        angle = 0

stars = []

zoom= -15.0
tilt= 90.0
spin= 0

loop=0
texture = 0

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(window_width, window_height, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, on_window_size)
    glfw.set_key_callback(window, key_callback)

    initGL(window)
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render here, e.g. using pyOpenGL
        display(window)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

def on_window_size(window, w, h):
    # get the frame buffer size and don't rely on the window
    # the window size and the framebuffer can vary on retina displays
    size_w, size_h = glfw.get_framebuffer_size(window)
    window_width = size_w
    window_height = size_h
    
    gl.glViewport(0, 0, window_width, window_height) #Reset The Current Viewport And Perspective Transformation

    gl.glMatrixMode(gl.GL_PROJECTION) #Select The Projection Matrix
    gl.glLoadIdentity() #Reset The Projection Matrix

    glu.gluPerspective(45.0,window_width/window_height,0.1,100.0) #Calculate The Aspect Ratio Of The Window
    gl.glMatrixMode(gl.GL_MODELVIEW) #Select The Modelview Matrix

def key_callback(window, key, scancode, action, mods):
    global twinkle, tilt, zoom

    if action == glfw.RELEASE:
        if key == glfw.KEY_T: 
            twinkle = not twinkle
        elif  key == glfw.KEY_UP:
            tilt -= 1.5
        elif key == glfw.KEY_DOWN:
            tilt += 1.5
        elif key == glfw.KEY_Z:
            zoom -= 0.2
        elif key == glfw.KEY_S:
            zoom += 0.2

def LoadTextures():
    global texture
    image = Image.open(os.path.join("Data", "Star.bmp"))
    
    sizeX = image.size[0]
    sizeY = image.size[1]

    texture = gl.glGenTextures(1) #Create The Texture

    #get the raw image pixel converted in openGL coordinates (point (0,0) is bottom, left)
    image = image.convert("RGBA").tobytes("raw", "RGBA", 0, -1)

    # Create Linear Filtered Texture
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, 3, sizeX, sizeY, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image) 

def initGL(window):
    global stars
    LoadTextures()

    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glShadeModel(gl.GL_SMOOTH) #Enables Smooth Color Shading

    gl.glClearColor(0.0,0.0,0.0,1.0) #black
    #gl.glClearColor(0.40,0.58,0.93,1.0) #cornflower blue
    gl.glClearDepth(1.0) #Enables Clearing Of The Depth Buffer

    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST) #Really Nice Perspective
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE) #Set The Blending Function For Translucency
    gl.glEnable(gl.GL_BLEND) #Enables Depth Testing

    for index in range(num):
        star = Star()
        star.angle = 0.0 #Start All The Stars At Angle Zero
        star.dist = (index / num) * 5.0
        star.r = random.randrange(1, 256, 1)
        star.g = random.randrange(1, 256, 1)
        star.b = random.randrange(1, 256, 1)
        stars.append(star)

    on_window_size(window, window_width, window_height)

def display(window):
    global zoom, tilt, stars, num, spin, texture
    
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture) # Select Our Texture

    for index in range(num):

        star = stars[index]

        gl.glLoadIdentity() # Reset The View Before We Draw Each Star
        gl.glTranslatef(0.0,0.0,zoom) #Zoom Into The Screen (Using The Value In 
        gl.glRotatef(tilt, 1.0, 0.0, 0.0) #Tilt The View (Using The Value In 'tilt')
        gl.glRotatef(star.angle, 0.0, 1.0, 0.0) #Rotate To The Current Stars Angle
        gl.glTranslatef(star.dist, 0.0, 0.0) #Move Forward On The X Plane
        gl.glRotatef(star.angle,0.0,1.0,0.0) #Cancel The Current Stars Angle
        gl.glRotatef(-tilt,1.0,0.0,0.0) #Cancel The Screen Tilt

        if twinkle : #if Twinkling is Enabled we draw an additional star

            # Assign A Color Using Bytes
            gl.glColor4ub(stars[(num-index)-1].r,stars[(num-index)-1].g,stars[(num-index)-1].b,255)
            gl.glBegin(gl.GL_QUADS) #Begin Drawing The Textured Quad
            gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f(-1.0,-1.0, 0.0);
            gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f( 1.0,-1.0, 0.0);
            gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f( 1.0, 1.0, 0.0);
            gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f(-1.0, 1.0, 0.0);
            gl.glEnd() #Done Drawing The Textured Quad

        # main star
        gl.glRotatef(spin, 0.0, 0.0, 1.0)       # rotate the star on the z axis.

        # Assign A Color Using Bytes
        gl.glColor4ub(star.r,star.g,star.b,255)
        gl.glBegin(gl.GL_QUADS)           # Begin Drawing The Textured Quad
        gl.glTexCoord2f(0.0, 0.0) 
        gl.glVertex3f(-1.0,-1.0, 0.0)
        gl.glTexCoord2f(1.0, 0.0) 
        gl.glVertex3f( 1.0,-1.0, 0.0)
        gl.glTexCoord2f(1.0, 1.0) 
        gl.glVertex3f( 1.0, 1.0, 0.0)
        gl.glTexCoord2f(0.0, 1.0) 
        gl.glVertex3f(-1.0, 1.0, 0.0)
        gl.glEnd()             # Done Drawing The Textured Quad

        spin +=0.01                           # used to spin the stars.
        star.angle += index * 1.0 / num * 1.0    # change star angle.
        star.dist  -= 0.01              # bring back to center.

        if star.dist < 0.0:             # star hit the center
            star.dist += 5.0            # move 5 units from the center.
            star.r = random.randrange(1, 256, 1)        # new red color.
            star.g = random.randrange(1, 256, 1)        # new green color.
            star.b = random.randrange(1, 256, 1)        # new blue color.

if __name__ == "__main__":
    main()
