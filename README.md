# Pokemon-Terminal

Pokemon terminal themes for iTerm2. Supports a total of 493 unique Pokemon.
![alt-tag](Samples/pikachu.png)

Sample Set #1                    |  Sample Set #2
:-------------------------------:|:-------------------------------:
![alt-tag](Samples/bulbasaur.png)|  ![alt-tag](Samples/squirtle.png)
![alt-tag](Samples/charizard.png)|  ![alt-tag](Samples/eevee.png)
![alt-tag](Samples/clefairy.png) |  ![alt-tag](Samples/magikarp.png)
![alt-tag](Samples/machop.png)   |  ![alt-tag](Samples/slowpoke.png)
![alt-tag](Samples/muk.png)      |  ![alt-tag](Samples/porygon.png)
![alt-tag](Samples/chansey.png)  |  ![alt-tag](Samples/growlithe.png)
![alt-tag](Samples/scyther.png)  |  ![alt-tag](Samples/omanyte.png)
![alt-tag](Samples/corsola.png)  |  ![alt-tag](Samples/mewtwo.png)
![alt-tag](Samples/azumarill.png)|  ![alt-tag](Samples/snubbull.png)
![alt-tag](Samples/wobbuffet.png)|  ![alt-tag](Samples/tyranitar.png)
![alt-tag](Samples/lugia.png)    |  ![alt-tag](Samples/kyogre.png)
![alt-tag](Samples/rayquaza.png) |  ![alt-tag](Samples/deoxys.png)

# How to Install

1. Make sure you have [Python 3.5](https://www.python.org/downloads/mac-osx/) or higher.
2. Make sure you have [iTerm2](http://www.iterm2.com/downloads.html). If you have homebrew you can install iTerm with the following command:
    ```
    brew cask install iterm2
    ```
3. Download the repository and unzip it.
4. Locate ~/.bash_profile and add the path to the repository so that it may be accessed from anywhere. Example:
    ```
    # Pokemon
    PATH="/Users/Laki/GitHub/Pokemon-Terminal:${PATH}"
    ```
5. Reload ~/.bash_profile so that the above changes are updated:
    ```
    $ source ~/.bash_profile
    ```
6. Now you can change the terminal background like so:
    ```
    $ pokemon pikachu
    ```

# Usage

```

Usage:
    pokemon [parameter]

Parameters:
    [name]      -   Change the terminal background to the specified Pokemon.
    [index]     -   Change the terminal background to a Pokemon by its index.
    [region]    -   List all the Pokemon of the specified region.
    [letter]    -   List all Pokemon who's names begin with a particular letter.

Other Parameters:
    pokemon all             -   List all the Pokemon supported.
    pokemon random          -   Pick a Pokemon at random.
    pokemon ?               -   Identify the current Pokemon.
    pokemon regions         -   List all the available regions.
    pokemon slideshow       -   Iterate through each Pokemon.
    pokemon slideshow-kanto -   Iterate through each Pokemon in the specified reigon.
    pokemon extra           -   List all the Pokemon from the 'Extra' folder.
    pokemon help            -   Display this menu.
    
```

Example:

![alt-tag](Samples/usage.gif)

# Suggestions

I highly suggest making the font colors black and the terminal window transparent. Some of the images have both light and dark colours and so it can be difficult to see the font sometimes. Transparency resolves this issue. Since *Pokemon Terminal* only changes the background, the transparency must be done manually:

1. Navigate to iTerm2 > Preferences > Profiles > Window
2. Set the transparency to the center value.
3. Hit the "blur" checkbox.
4. Set the blur to maximum.

![alt-tag](Samples/transparency_setting.png)

# Adding Custom Images

The folder Images/Extra is for adding custom images. You can manually add backgrounds to this folder and they will be visible to the program. Only PNG format is supported. To see a list of all the custom backgrounds type:
```
pokemon extra
```
Alternatively, you can delete images from this folder and it will not break the program.

# Solutions for Issues

If you experience a line at the top of the terminal after changing the Pokemon, you can remove it by typing in the *clear* command or opening a new terminal.
![alt-tag](Samples/line.png)

# Notes

- Nearly all of the Pokemon backgrounds were created by [Teej](https://pldh.net/gallery/the493).
- Originally the images were about 100mb in total but I used [pngquant](https://pngquant.org/) to compress them down to about 30mb.
- Since the images are compressed a *few* of them have some mild compression artifacts that are noticeable if the terminal is in full screen.
