#!/usr/bin/env python

import os
import glfw
import OpenGL.GL as gl
import OpenGL.GLU as glu
import PIL.Image as Image

window_width = 640
window_height = 480

light = False
blend = False
xrot = 0.0
yrot = 0.0
xspeed = 0
yspeed = 0
z = -5.0

lightAmbient = gl.GLfloat_4(0.5, 0.5, 0.5, 1.0)
lightDiffuse = gl.GLfloat_4(1.0,1.0,1.0,1.0)
lightPosition = gl.GLfloat_4(0.0, 0.0, 2.0, 1.0)

filterIndex = 0
textures = []

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

def key_callback(window, key, scancode, action, mods):
    global xspeed, yspeed, light, filterIndex, textures, blend

    if action == glfw.RELEASE:
        if key == glfw.KEY_F: 
            filterIndex += 1
            filterIndex %= len(textures)
        elif key == glfw.KEY_L: 
            light = not light
            if not light:
                gl.glDisable(gl.GL_LIGHTING)
                gl.glDisable(gl.GL_LIGHT1)
            else:
                gl.glEnable(gl.GL_LIGHTING)
                gl.glEnable(gl.GL_LIGHT1)
        elif key == glfw.KEY_B:
            blend = not blend
            if blend:
                gl.glEnable(gl.GL_BLEND)
                gl.glDisable(gl.GL_DEPTH_TEST)
            else:
                gl.glDisable(gl.GL_BLEND)
                gl.glEnable(gl.GL_DEPTH_TEST)
        elif key == glfw.KEY_UP:
            xspeed -= 0.01
        elif key == glfw.KEY_DOWN:
            xspeed += 0.01
        elif key == glfw.KEY_RIGHT:
            yspeed += 0.01
        elif key == glfw.KEY_LEFT:
            yspeed -= 0.01


def LoadTextures():
    global textures
    image = Image.open(os.path.join("Data", "glass.bmp"))
    
    sizeX = image.size[0]
    sizeY = image.size[1]

    textures = gl.glGenTextures(3) #Create The Texture

    #get the raw image pixel converted in openGL coordinates (point (0,0) is bottom, left)
    image = image.convert("RGBX").tobytes("raw", "RGBX", 0, -1)
    
    # Create Nearest Filtered Texture
    gl.glBindTexture(gl.GL_TEXTURE_2D, textures[0])
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, 3, sizeX, sizeY, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image)

    # Create Linear Filtered Texture
    gl.glBindTexture(gl.GL_TEXTURE_2D, textures[1])
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, 3, sizeX, sizeY, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image)

    # Create MipMapped Texture
    gl.glBindTexture(gl.GL_TEXTURE_2D, textures[2])
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_NEAREST)
    glu.gluBuild2DMipmaps(gl.GL_TEXTURE_2D, gl.GL_RGBA, sizeX, sizeY, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image)  

def initGL(window):
    global lightAmbient, lightDiffuse, lightPosition
    LoadTextures()

    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glShadeModel(gl.GL_SMOOTH) #Enables Smooth Color Shading

    gl.glClearColor(0.40,0.58,0.93,1.0) #cornflower blue
    gl.glClearDepth(1.0) #Enables Clearing Of The Depth Buffer

    gl.glEnable(gl.GL_DEPTH_TEST) #Enables Depth Testing
    gl.glDepthFunc(gl.GL_LEQUAL) #The Type Of Depth Test To Do
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST) #Really Nice Perspective

    gl.glEnable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_LIGHT1)

    gl.glLightfv(gl.GL_LIGHT1, gl.GL_AMBIENT, lightAmbient) #Setup The Ambient Light
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_DIFFUSE, lightDiffuse) #Setup The Diffuse Light
    gl.glLightfv(gl.GL_LIGHT1, gl.GL_POSITION, lightPosition) #Position The Light

    gl.glColor4f(1.0,1.0,1.0,0.5) #Full Brightness, 50% Alpha
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE) #Blending Function For Translucency Based On Source Alpha 

    on_window_size(window, window_width, window_height)

def display():
    global xrot, yrot, z, xspeed, yspeedtextures, filterIndex, light
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    gl.glLoadIdentity()
    gl.glTranslatef(0.0,0.0,z) # Translate Into/Out Of The Screen By z
    gl.glRotatef(xrot,1.0,0.0,0.0) # Rotate On The X Axis By xrot
    gl.glRotatef(yrot,0.0,1.0,0.0) # Rotate On The Y Axis By yrot

    gl.glBindTexture(gl.GL_TEXTURE_2D, textures[filterIndex]) # Select Our Texture

    gl.glBegin(gl.GL_QUADS)

    # Front Face
    gl.glNormal3f(0.0, 0.0, 1.0) # Normal Pointing Towards Viewer
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f(-1.0, -1.0,  1.0)  # Bottom Left Of The Texture and Quad
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f( 1.0, -1.0,  1.0)  # Bottom Right Of The Texture and Quad
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f( 1.0,  1.0,  1.0)  # Top Right Of The Texture and Quad
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f(-1.0,  1.0,  1.0)  # Top Left Of The Texture and Quad
    # Back Face
    gl.glNormal3f(0.0, 0.0,-1.0) # Normal Pointing Away From Viewer
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f(-1.0, -1.0, -1.0)  # Bottom Right Of The Texture and Quad
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f(-1.0,  1.0, -1.0)  # Top Right Of The Texture and Quad
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f( 1.0,  1.0, -1.0)  # Top Left Of The Texture and Quad
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f( 1.0, -1.0, -1.0)  # Bottom Left Of The Texture and Quad
    # Top Face
    gl.glNormal3f( 0.0, 1.0, 0.0) # Normal Pointing Up
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f(-1.0,  1.0, -1.0)  # Top Left Of The Texture and Quad
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f(-1.0,  1.0,  1.0)  # Bottom Left Of The Texture and Quad
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f( 1.0,  1.0,  1.0)  # Bottom Right Of The Texture and Quad
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f( 1.0,  1.0, -1.0)  # Top Right Of The Texture and Quad
    # Bottom Face
    gl.glNormal3f( 0.0,-1.0, 0.0) # Normal Pointing Down
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f(-1.0, -1.0, -1.0)  # Top Right Of The Texture and Quad
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f( 1.0, -1.0, -1.0)  # Top Left Of The Texture and Quad
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f( 1.0, -1.0,  1.0)  # Bottom Left Of The Texture and Quad
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f(-1.0, -1.0,  1.0)  # Bottom Right Of The Texture and Quad
    # Right face
    gl.glNormal3f( 1.0, 0.0, 0.0) # Normal Pointing Right
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f( 1.0, -1.0, -1.0)  # Bottom Right Of The Texture and Quad
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f( 1.0,  1.0, -1.0)  # Top Right Of The Texture and Quad
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f( 1.0,  1.0,  1.0)  # Top Left Of The Texture and Quad
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f( 1.0, -1.0,  1.0)  # Bottom Left Of The Texture and Quad
    # Left Face
    gl.glNormal3f(-1.0, 0.0, 0.0) # Normal Pointing Left
    gl.glTexCoord2f(0.0, 0.0); gl.glVertex3f(-1.0, -1.0, -1.0)  # Bottom Left Of The Texture and Quad
    gl.glTexCoord2f(1.0, 0.0); gl.glVertex3f(-1.0, -1.0,  1.0)  # Bottom Right Of The Texture and Quad
    gl.glTexCoord2f(1.0, 1.0); gl.glVertex3f(-1.0,  1.0,  1.0)  # Top Right Of The Texture and Quad
    gl.glTexCoord2f(0.0, 1.0); gl.glVertex3f(-1.0,  1.0, -1.0)  # Top Left Of The Texture and Quad
    gl.glEnd()

    xrot+=xspeed # xspeed To xrot
    yrot+=yspeed # Add yspeed To yrot

if __name__ == "__main__":
    main()
