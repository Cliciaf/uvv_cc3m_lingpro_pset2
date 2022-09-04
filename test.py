#!/usr/bin/env python3

import os
from unittest import result
import pset2
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)

class TestImage(unittest.TestCase):
    def test_load(self):
        result = pset2.Image.load('imagens_teste/pixel_centralizado.png')
        expected = pset2.Image(11, 11,
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(result, expected)


class TestInverted(unittest.TestCase):
    def test_inverted_1(self):
        im = pset2.Image.load('imagens_teste/pixel_centralizado.png')
        result = im.inverted()
        expected = pset2.Image(11, 11,
                             [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255])
        self.assertEqual(result,  expected)

    def test_inverted_2(self):
        im = pset2.Image(4,1,[29, 89, 136, 200])
        result = im.inverted()
        expected = pset2.Image(4,1,
                                [226,166,119,55])
        self.assertTrue(result, expected)

    def test_inverted_images(self):
        for fname in ('cogumelo', 'gatos', 'xadrez'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'imagens_teste', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'resultados_teste', '%s_invertido.png' % fname)
                result = pset2.Image.load(inpfile).inverted()
                expected = pset2.Image.load(expfile)
            self.assertEqual(result,  expected)


class TestFilters(unittest.TestCase):
    def test_blurred(self):
        for kernsize in (1, 3, 7):
            for fname in ('cogumelo', 'gatos', 'xadrez'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'imagens_teste', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'resultados_teste', '%s_blur_%02d.png' % (fname, kernsize))
                    input_img = pset2.Image.load(inpfile)
                    input_img_copy = pset2.Image(input_img.width, input_img.height, input_img.pixels)
                    result = input_img.blurred(kernsize)
                    expected = pset2.Image.load(expfile)
                    self.assertEqual(input_img, input_img_copy, "Be careful not to modify the original image!")
                    self.assertEqual(result,  expected)

    def test_sharpened(self):
        for kernsize in (1, 3, 9):
            for fname in ('cogumelo', 'gatos', 'xadrez'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'imagens_teste', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'resultados_teste', '%s_sharp_%02d.png' % (fname, kernsize))
                    input_img = pset2.Image.load(inpfile)
                    input_img_copy = pset2.Image(input_img.width, input_img.height, input_img.pixels)
                    result = input_img.sharpened(kernsize)
                    expected = pset2.Image.load(expfile)
                    self.assertEqual(input_img, input_img_copy, "Be careful not to modify the original image!")
                    self.assertEqual(result,  expected)

    def test_edges(self):
        for fname in ('cogumelo', 'gatos', 'xadrez'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'imagens_teste', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'resultados_teste', '%s_edges.png' % fname)
                input_img = pset2.Image.load(inpfile)
                input_img_copy = pset2.Image(input_img.width, input_img.height, input_img.pixels)
                result = input_img.edges()
                expected = pset2.Image.load(expfile)
                self.assertEqual(input_img, input_img_copy, "Be careful not to modify the original image!")
                self.assertEqual(result,  expected)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
