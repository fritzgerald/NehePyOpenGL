#!/usr/bin/env python

import glfw
import OpenGL.GL as gl
import OpenGL.GLU as glu

window_width = 640
window_height = 480

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

def initGL(window):
    gl.glClearColor(0.40,0.58,0.93,1.0) #cornflower blue

    gl.glClearDepth(1.0) #Enables Clearing Of The Depth Buffer
    gl.glDepthFunc(gl.GL_LESS) #The Type Of Depth Test To Do
    gl.glEnable(gl.GL_DEPTH_TEST) #Enables Depth Testing

    gl.glShadeModel(gl.GL_SMOOTH) #Enables Smooth Color Shading

    on_window_size(window, window_width, window_height)

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    gl.glLoadIdentity()
    gl.glTranslatef(-1.5,0.0,-6.0)

    gl.glBegin(gl.GL_TRIANGLES)

    gl.glVertex3f( 0.0, 1.0, 0.0)
    gl.glVertex3f(-1.0,-1.0, 0.0)
    gl.glVertex3f( 1.0,-1.0, 0.0)

    gl.glEnd()

    gl.glLoadIdentity()
    gl.glTranslatef(1.5,0.0,-6.0)

    gl.glBegin(gl.GL_QUADS)
    gl.glVertex3f(-1.0, 1.0, 0.0)
    gl.glVertex3f( 1.0, 1.0, 0.0)
    gl.glVertex3f( 1.0,-1.0, 0.0)
    gl.glVertex3f(-1.0,-1.0, 0.0)
    gl.glEnd()

if __name__ == "__main__":
    main()