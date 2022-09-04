#!/usr/bin/env python3

from operator import invert
import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as PILImage

## NO ADDITIONAL IMPORTS ALLOWED!

class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    def get_pixel(self, x, y):
        if x<0:
           x = 0 
        elif x>=self.width:
            x=self.width - 1

        if y<0:
            y = 0
        elif y>=self.height:
            y = self.height - 1
        return self.pixels[(x+y*self.width)]


    def fix_pixel(self):
        """função que garante que todos os pixels da imagem sejam INTEIROS"""
        for x in range(self.width):
            for y in range(self.height):
                take_pixel = self.get_pixel(x,y)
                if take_pixel < 0:
                    take_pixel = 0
                elif take_pixel > 255:
                    take_pixel = 255
                take_pixel = round(take_pixel)
                self.set_pixel(x,y, take_pixel)

    def set_pixel(self, x, y, c):
        self.pixels[(x+y*self.width)] = c

    def apply_per_pixel(self, func):
        result = Image.new(self.width, self.height)
        for x in range(result.width):
            for y in range(result.height):
                color = self.get_pixel(x, y)
                newcolor = func(color)
                result.set_pixel(x,y, newcolor)
        return result

    def inverted(self):
        """inverte o valor do pixel"""
        return self.apply_per_pixel(lambda c: 255-c)

    def blurred(self, n):
        """gera o kernel de desfoque"""
        kernel = self.correlation(kernelGenerator(n))
        kernel.fix_pixel()
        return kernel

    def sharpened(self, n):
        """filtro que deixa a imagem mais nitida"""
        im_bur = self.blurred(n)
        im = Image.new(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                sharp = round(2*self.get_pixel(x,y)-(im_bur.get_pixel(x,y)))
                im.set_pixel(x,y, sharp)
        im.fix_pixel()
        return im


    def edges(self):
        """detecta as bordas da imagem """
        im = Image.new(self.width, self.height)
        kernelX = [[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]
        kernelY = [[-1, -2, -1],[0, 0, 0],[1, 2, 1]]
        save_kernelX = self.correlation(kernelX)
        save_kernelY = self.correlation(kernelY)
        for x in range(self.width):
            for y in range(self.height):
                cor = round (math.sqrt(save_kernelX.get_pixel(x,y)**2 + save_kernelY.get_pixel(x,y)**2 ))
                im.set_pixel(x,y,cor) 
        im.fix_pixel       
        return im

    def correlation(self,kernel):
        """aplica o kernel na imagem"""
        width_kernel = len(kernel)
        im = Image.new(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                newcolor = 0
                for i in range(width_kernel):
                    for j in range(width_kernel):
                        newcolor += self.get_pixel((x-(width_kernel//2)+j),(y-(width_kernel//2)+i))*kernel[i][j]
                im.set_pixel(x,y,newcolor)
        return im




    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    def __repr__(self):
        return "Image(%s, %s, %s)" % (self.width, self.height, self.pixels)

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))

        # when the window is closed, the program should stop
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)

def kernelGenerator(n):
    kernel = [[1/n**2 for index in range(n)]for index in range(n)]
    return kernel
                


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass 

    #alguns meios para obter as imagens para as questões
    #questão6
    #novaImag = Image.load('imagens_teste/obra.png')
    #edge = novaImag.edges()
    #edge.show()
    #edge.save('resultados/obra2.png')
    #questão 2
    #keepInverted = novaImag.inverted()
    #keepInverted.save('resultados/questão2.png')
    #questão 4
    #kernel = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #            [1, 0, 0, 0, 0, 0, 0, 0, 0], 
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    #keepCorrelation = novaImag.correlation(kernel)
    #keepCorrelation.save('resultados/questão4.png')

    # Questão 5
    # kernel1 = [[0, 0, 0], 
    #            [0, 2, 0], 
    #            [0, 0, 0]]
    # kernel2 = [[1/9, 1/9, 1/9], 
    #            [1/9, 1/9, 1/9], 
    #            [1/9, 1/9, 1/9]]
    # subtraindo o kernel1 pelo kernel2
    # kernelResult = [[-1/9, -1/9, -1/9],
    #                 [-1/9, 17/9, -1/9],
    #                 [-1/9, -1/9, -1/9]]
    # i = Image.load('test_images/python.png')
    # focado = i.correlacao(kernelResult)
    # focado.show()
    # i.show()

    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
