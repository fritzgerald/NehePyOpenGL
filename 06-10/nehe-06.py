#!/usr/bin/env python

import os
import glfw
import OpenGL.GL as gl
import OpenGL.GLU as glu
import PIL.Image as Image

window_width = 640
window_height = 480

xrot = 0.0
yrot = 0.0
zrot = 0.0
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

    initGL(window)
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render here, e.g. using pyOpenGL
        display()

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

def LoadTextures():
    global texture
    image = Image.open(os.path.join("Data", "NeHe.bmp"))
    
    ix = image.size[0]
    iy = image.size[1]

    texture = gl.glGenTextures(1) #Create The Texture
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture) # Typical Texture Generation Using Data From The Bitmap

    #get the raw image pixel converted in openGL coordinates (point (0,0) is bottom, left)
    image = image.tobytes("raw", "RGBX", 0, -1)
    
    # glTexImage2D(target, levelOfDetail, numberOfColorComponents, width, height, border, format, type, data)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, 3, ix, iy, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image) # Generate The Texture

    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR) # Linear Filtering
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR) # Linear Filtering

def initGL(window):
    LoadTextures()

    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glShadeModel(gl.GL_SMOOTH) #Enables Smooth Color Shading

    gl.glClearColor(0.40,0.58,0.93,1.0) #cornflower blue
    gl.glClearDepth(1.0) #Enables Clearing Of The Depth Buffer

    gl.glEnable(gl.GL_DEPTH_TEST) #Enables Depth Testing
    gl.glDepthFunc(gl.GL_LEQUAL) #The Type Of Depth Test To Do
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST) #Really Nice Perspective 

    on_window_size(window, window_width, window_height)

def display():
    global xrot, yrot, zrot, texture
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    gl.glLoadIdentity()
    gl.glTranslatef(0.0,0.0,-5.0) #Move Into The Screen 5 Units

    gl.glRotatef(xrot,1.0,0.0,0.0) # Rotate On The X Axis
    gl.glRotatef(yrot,0.0,1.0,0.0) # Rotate On The Y Axis
    gl.glRotatef(zrot,0.0,0.0,1.0) # Rotate On The Z Axis

    gl.glBindTexture(gl.GL_TEXTURE_2D, texture) # Select Our Texture

    gl.glBegin(gl.GL_QUADS)

    # Front Face
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f(-1.0, -1.0,  1.0)  # Bottom Left Of The Texture and Quad
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f( 1.0, -1.0,  1.0)  # Bottom Right Of The Texture and Quad
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f( 1.0,  1.0,  1.0)  # Top Right Of The Texture and Quad
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f(-1.0,  1.0,  1.0)  # Top Left Of The Texture and Quad
    # Back Face
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f(-1.0, -1.0, -1.0)  # Bottom Right Of The Texture and Quad
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f(-1.0,  1.0, -1.0)  # Top Right Of The Texture and Quad
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f( 1.0,  1.0, -1.0)  # Top Left Of The Texture and Quad
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f( 1.0, -1.0, -1.0)  # Bottom Left Of The Texture and Quad
    # Top Face
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f(-1.0,  1.0, -1.0)  # Top Left Of The Texture and Quad
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f(-1.0,  1.0,  1.0)  # Bottom Left Of The Texture and Quad
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f( 1.0,  1.0,  1.0)  # Bottom Right Of The Texture and Quad
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f( 1.0,  1.0, -1.0)  # Top Right Of The Texture and Quad
    # Bottom Face
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f(-1.0, -1.0, -1.0)  # Top Right Of The Texture and Quad
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f( 1.0, -1.0, -1.0)  # Top Left Of The Texture and Quad
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f( 1.0, -1.0,  1.0)  # Bottom Left Of The Texture and Quad
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f(-1.0, -1.0,  1.0)  # Bottom Right Of The Texture and Quad
    # Right face
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f( 1.0, -1.0, -1.0)  # Bottom Right Of The Texture and Quad
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f( 1.0,  1.0, -1.0)  # Top Right Of The Texture and Quad
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f( 1.0,  1.0,  1.0)  # Top Left Of The Texture and Quad
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f( 1.0, -1.0,  1.0)  # Bottom Left Of The Texture and Quad
    # Left Face
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f(-1.0, -1.0, -1.0)  # Bottom Left Of The Texture and Quad
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f(-1.0, -1.0,  1.0)  # Bottom Right Of The Texture and Quad
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f(-1.0,  1.0,  1.0)  # Top Right Of The Texture and Quad
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f(-1.0,  1.0, -1.0)  # Top Left Of The Texture and Quad
    gl.glEnd()

    xrot+=0.3 # X Axis Rotation
    yrot+=0.2 # Y Axis Rotation
    zrot+=0.4 # Z Axis Rotation

if __name__ == "__main__":
    main()