## Convert SVG files to PNG based on [svgexport][svgexport]

[svgexport][svgexport] is a Node.js module and command-line tool for exporting SVG files to PNG and JPEG, it uses PhantomJS for rendering SVG files.

## Use in python

First install it via [npm][npm]

```bash
npm install svgexport -g
```

Then run `svg2png.py`

- Convert one
    ```bash
    python svg2png.py <input.svg> [-o output.png]
    ```

- Convert from directory
    ```bash
    python svg2png.py -d <input_dir> [-o output_dir]
    ```

> Modify line 15 of `svg2png.py` follow the svgexport usage if you want.

For example

- Convert one
    ```bash
    python svg2png.py ./fontawesome-free-5.4.1-desktop-svgs/brands/500px.svg -o ./pngs/brands_32/500px.png
    ```

- Convert from directory
    ```bash
    python svg2png.py -d ./fontawesome-free-5.4.1-desktop-svgs/brands -o ./pngs/brands_32
    python svg2png.py -d ./fontawesome-free-5.4.1-desktop-svgs/regular -o ./pngs/regular_32
    python svg2png.py -d ./fontawesome-free-5.4.1-desktop-svgs/solid -o ./pngs/solid_32
    ```

[svgexport]: https://github.com/shakiba/svgexport
[npm]: https://www.npmjs.com/