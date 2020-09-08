# FIR
FIR Programming Language

Yep this is a programming language made intirely in Python.

It has assembly style syntax nothing crazy.

# Download
Clone it or download the zip, unpack it, make sure you have python 3.7 or above,
then type this in the command line (same directory where you stored it)

`python fir.py <file-PATH>`
Here the file is the file you want to execute.

# Example
Here is a quick example (save it as ex1.fir')

```
; Add two numbers
ldx 10
ldy 5
add
out a
```

Then run the command:

`python fir.py ex1.fir`
