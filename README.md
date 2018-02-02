QR Code SVG Generator for CrypTile
==================================
Generate etch-ready logos for the CrypTile project!  Learn how at https://CrypTile.us

Turn this...
![Example Code](https://github.com/george-viaud/QR-Code-SVG-Logo-Generator/raw/gh-pages/sample.png)
Into this...
![Example Code](https://raw.githubusercontent.com/george-viaud/QR-Code-SVG-Logo-Generator/gh-pages/prototype_red.png)

Logo should be a svg file, the output QR code is also an SVG

Simply pass the svg file containing the logo, the url you want on the QR code, and the output filename

Since the addition of a logo reduces redundancy, you may wish to produce tiles without a logo, depending on your threat model.

```
./generate.py ./coin-logos/BTC.svg "correct horse battery staple pacifist convolve pinch amputate upstream potsherd baryta nod" ./your_seed.svg
```
or
```
./generate.py --nologo "correct horse battery staple pacifist convolve pinch amputate upstream potsherd baryta nod" ./your_seed.svg
```

Dependencies
------------
Python modules:
PIL (Python Imaging Library)
