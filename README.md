# ADAW - A DAW

ADAW is a shitty daw-as-a-library, written in python and numpy.
Currently only 44.1 16bit WAV files are supported, both for input and output. Please convert any files to WAV before feeding it in to your program.

ADAW is made up of 4 "sub-modules":
- *lib* - Contains `Project` and `Clip`, the two essential classes for creating music.
- *builtin* - Contains wave functions
- *effects* - Contains effects
- *lily* - Lilypond-like language parser for speedy music production

I'm too lazy to document things just yet so you can either figure everything out yourself or wait for me to add documentation

# TODO

- Add phase calculation to functions in `lily` to prevent that popping noise whenever the wave jumps a significant amount
