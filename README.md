# CreamPy

A set of tools that help you de-duplicate images that differ slightly.

Project Goals
=============
- Support BMP, JPEG, and PNG.
- Create diffs between images.
- Automatically group together the most similar images.
- Build a graph of images such that changes between images in a set that occur 
  in more than one pair of images need only be stored once.
- Recreate the original image set with no loss of data.
- Preview base images easily.
- Ultimately, define a format that can be used to reliably store a de-duplicated
  data set.
- Perform benchmarks against popular archive formats.




Why?
====

I have lots of BMP, JPEG, and PNG image sets that are largely the same image 
duplicated and modified. 

- PNG

In the case of PNG images, each image is compressed individually with zlib. 
Small changes to individual images produce wildly different ouputs, making it 
difficult for lossless compression algorithms to find the hidden redundancy.
At the moment I can convert my PNGs to BMP and *then* compress them as a
solid archive, but then file previews are impossible without decompressing 
the entire archive up to that point.

- JPEG

In the case of JPEG images, an unscientific test in which I losslessly
compressed two similar JPEG files into one LZMA archive saved only 3% space.
Realistically speaking, the creators of these images are saving these with the
same quality settings and optimizations, so the MCUs should be identical. At the
very least, opening them in an image editor reveals that each 8x8 pixel block
is, in fact, identical in most areas. I don't know what tripped up LZMA in this
case.

- BMP

This one should be fairly obvious by now.
