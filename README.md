# Pokemon-Terminal

[![Build Status](https://travis-ci.org/LazoCoder/Pokemon-Terminal.svg?branch=master)](https://travis-ci.org/LazoCoder/Pokemon-Terminal)

<p align="center">
    <img src="https://i.imgur.com/n34fXyp.png" width="300"/>
    <img src="https://i.imgur.com/xaHPMUd.png" width="300"/>
</p>

[More previews](https://imgur.com/a/0wfFm)

# Features
- 719 unique Pokemon
- Select Pokemon by name or by index number
- Ability to change the Desktop Wallpaper & the Terminal background
- Internal search system for finding Pokemon
- Supports iTerm2, Terminology & Tilix

# Installation

Install Python 3.6 or higher:
- [For Mac](https://www.python.org/downloads/mac-osx/)
- [For Ubuntu](https://askubuntu.com/a/865569)
- [For Arch Linux](https://www.archlinux.org/packages/extra/x86_64/python/)
- Not all compatible distros are named here, but a quick Google search should give you instructions for your distribution of choice.

Get a compatible terminal emulator:
- [iTerm2](https://iterm2.com/)
- [Terminology](https://www.enlightenment.org/about-terminology)
- [Tilix](https://gnunn1.github.io/tilix-web/)

You can then proceed with one of the following methods for installation:
- [Arch Linux User Repository package (System-wide)](https://aur.archlinux.org/packages/pokemon-terminal-git/) (maintained by [@sylveon](https://github.com/sylveon))
- [pip (System-wide)](#pip-system-wide)
- [pip (Per-User)](#pip-per-user)
- [npm (Per-User)](#npm-per-user)
- [Distutils (System-wide)](#distutils-system-wide)

Notes:
- Your distro might include pip in a different package then Python, make sure to have that installed and running when calling `pip3.6` if you want to install using it.
- npm installation obviously requires to have [Node.js](https://nodejs.org/) installed.

## pip (System-wide)

Run `sudo pip3.6 install git+https://github.com/LazoCoder/Pokemon-Terminal.git`. When the command completes, it's installed and ready to go!

## pip (Per-User)

You can install it with pip for a single user with `pip3.6 install --user git+https://github.com/LazoCoder/Pokemon-Terminal.git`. You might want to add `~/.local/bin` to your PATH to be able to call `pokemon` and `ichooseyou` everywhere.

## npm (Per-User)

You can install in any (npm-supported) OS using `npm install --global pokemon-terminal`. That's it, you're done!

## Distutils (System-wide)

You can clone or [download](https://github.com/LazoCoder/Pokemon-Terminal/archive/master.zip) this repo, and run `sudo python3.6 setup.py install` at the root of the repo.

# Usage

```
usage: pokemon [-h] [-n NAME]
               [-r [{kanto,johto,hoenn,sinnoh,unova,kalos} [{kanto,johto,hoenn,sinnoh,unova,kalos} ...]]]
               [-l [0.xx]] [-d [0.xx]]
               [-t [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} ...]]]
               [-ne] [-e] [-ss [X]] [-w] [-v] [-dr] [-c]
               [id]

Set a pokemon to the current terminal background or wallpaper

positional arguments:
  id                    Specify the wanted pokemon ID or the exact (case
                        insensitive) name

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear           Clears the current pokemon from terminal background
                        and quits.

Filters:
  Arguments used to filter the list of pokemons with various conditions that
  then will be picked

  -n NAME, --name NAME  Filter by pokemon which name contains NAME
  -r [{kanto,johto,hoenn,sinnoh,unova,kalos} [{kanto,johto,hoenn,sinnoh,unova,kalos} ...]], --region [{kanto,johto,hoenn,sinnoh,unova,kalos} [{kanto,johto,hoenn,sinnoh,unova,kalos} ...]]
                        Filter the pokemons by region
  -l [0.xx], --light [0.xx]
                        Filter out the pokemons darker (ligthness treshold
                        lower) then 0.xx (default is 0.7)
  -d [0.xx], --dark [0.xx]
                        Filter out the pokemons lighter (ligthness treshold
                        higher) then 0.xx (defualt is 0.42)
  -t [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} ...]], --type [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} [{normal,fire,fighting,water,flying,grass,poison,electric,ground,psychic,rock,ice,bug,dragon,ghost,dark,steel,fairy} ...]]
                        Filter the pokemons by type.
  -ne, --no-extras      Excludes extra pokemons (from the extras folder)
  -e, --extras          Excludes all non-extra pokemons

Misc:
  -ss [X], --slideshow [X]
                        Instead of simply choosing a random pokemon from the
                        filtered list, starts a slideshow (with X minutes of
                        delay between pokemon) in the background with the
                        pokemon that matched the filters
  -w, --wallpaper       Changes the desktop wallpaper instead of the terminal
                        background
  -v, --verbose         Enables verbose output
  -dr, --dry-run        Implies -v and doesnt actually changes either
                        wallpaper or background after the pokemon has been
                        chosen

Not setting any filters will get a completely random pokemon
```

Example:

![](https://i.imgur.com/DfA2lcd.gif)

# Tips, tricks and common issues

## iTerm2 settings

I highly suggest making the font colors black and the terminal window transparent. Some of the images have both light and dark colours and so it can be difficult to see the text sometimes. Transparency resolves this issue. Since *Pokemon-Terminal* only changes the background, the transparency must be done manually:

1. Navigate to iTerm2 > Preferences > Profiles > Window
2. Set the transparency to about half way.
3. Hit the "blur" checkbox.
4. Set the blur to maximum.
5. Optionally you can set the blending to maximum to adjust the colors to look like the samples provided.

![](https://i.imgur.com/xSZAGhL.png)

The result should look like this:

![](https://i.imgur.com/82DAT97.jpg)

## Adding Custom Images

The folder `pokemonterminal/Images/Extra` is for adding custom images. You can manually add backgrounds to this folder and they will be visible to the program. Only JPG format is supported. To see a list of all the custom backgrounds type:
```bash
$ pokemon -e -dr
```
Alternatively, you can delete images from this folder and it will not break the program. These are some custom backgrounds:

![](https://i.imgur.com/gdGUucu.gif)

## Solutions for Common Issues

* If you experience a line at the top of the terminal after changing the Pokemon, you can remove it by typing in the `clear` command or opening a new terminal.
![](https://i.imgur.com/5HMu1jD.png)

* If you are using Tilix and the terminal background is not changing, try adjusting the transparency in your profile settings.
* If you are experiencing issues with Terminology and are running on Ubuntu, make sure that you have installed the latest version:
   ```bash
   $ sudo add-apt-repository ppa:niko2040/e19
   $ sudo apt-get update
   $ sudo apt install terminology
   ```
* If you get the error `39:46: syntax error: Expected end of line but found identifier. (-2741)`: Locate the file `ITerm.py` in `pokemonterminal/adapter/implementations` and on line 7, change `iTerm` to `iTerm2`. If you still experience the error, try changing it to `iTerm 2`.

## Saving

### macOS
I have not yet implemented a way to save the terminal background to a profile. To save a background you will need to setup a startup command in the profile.
1. Navigate to iTerm2 > Preferences > General
2. Locate the field where it says *Send text at start* under *Command*.
3. In that field type "pokemon -n [pokemon name]". You can see an example in the image down below.
   - Alternatively you can also type "pokemon" for a random theme each time you open up a new terminal.
4. You can leave out "; clear" if you don't care about the line showing up at the top of the terminal.

![](https://i.imgur.com/2d4qa9j.png)

### Linux
Terminology already saves it automatically, just untick "temporary" in the settings after setting your desired pokemon:
![](http://i.imgur.com/BTqYXKa.png)

To setup a random pokemon each session:
1. Open `~/.bashrc` in your favorite text editor.
2. Add the following lines to it:
   ```bash
   if [[ "$TERMINOLOGY" -eq "1" ]]; then
       pokemon
   fi
   ```
That will simply pick a completely random pokemon each session, but the `pokemon` line is simply calling the app, so you can still filter with regions, darkness, and etc. like you normally would, or you can also reset to a preset pokemon everytime you start.

# Notes & Credits

- Nearly all of the Pokemon backgrounds were created by [Teej](https://pldh.net/gallery/the493).
- Originally the images were about 100mb in total but [ImageOptim](https://imageoptim.com/) was used to compress them down to about 17mb.
- Since the images are compressed, some of them may have some mild (but negligible) compression artifacts.
- Thanks to [@DrMartinLutherXing](https://github.com/DrMartinLutherXing) for some bug fixes.
- Thanks to [@joanbono](https://github.com/joanbono) for the easy installation script in the readme.
- Thanks to [@BnMcG](https://github.com/BnMcG) for the region specific randomize function.
- Thanks to [@samosaara](https://github.com/samosaara) for the Linux (GNOME and Terminology) port.
- Thanks to [@sylveon](https://github.com/sylveon) for maintaining the AUR package.
- Thanks to [@therealklanni](https://github.com/therealklanni) for adding the project to npm.
- Thanks to [@MattMattV](https://github.com/MattMattV) for adding Tilix support.
- Thanks to [@connordinho](https://github.com/connordinho) for enhancing the slideshow functionality.
- Thanks to [@cclauss](https://github.com/cclauss) for simplifying the code in the database class and the main class.
- Thanks to [@Fiskie](https://github.com/Fiskie) for implementing the adapter design pattern, piping commands and more.
- Thanks to [@marcobiedermann](https://github.com/marcobiedermann) for better image compression.
- Thanks to [@kamil157](https://github.com/kamil157) and [@dosman711](https://github.com/dosman711) for the randomized slideshow function.
- Thanks to [@Squirrels](https://github.com/Squirrels) for adding Pokemon from the Unova and Kalos regions.
- Thanks to [@caedus75](https://github.com/caedus75) for pip and reorganizing the files & folders.
