# svg-to-dia

[Dia](http://dia-installer.de/) is an open-source diagram editor.
It supports [SVG pictograms](http://dia-installer.de/shapes/index.html).
**svg-to-dia** converts ordinary SVG in the format supported by Dia.

# How to use

- Prepare files:
```
svg-to-dia --name my-shapes my-file1.svg my-file2.svg my-file3.svg
```
the above command will create a sheets/ and a shapes/ folders.

- Move the generated files to dia's folder
```
mv sheets/* ~/.dia/sheets
mv shapes/* ~/.dia/shapes
```

- Don't forget to restart dia
- If you intend to publish, make sure to edit the `.sheet` files to add human-readable descriptions (multiple languages if you can)
- ... and to edit the `.shape` files to add better coordinates of attachment points

# Requirements
- Python
- ImageMagick

# License
svg-to-dia is released in the public domain, see [UNLICENSE file](UNLICENSE).
