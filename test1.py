import time
import fluidsynth

fs = fluidsynth.Synth()
fs.start(driver="alsa")
## Your installation of FluidSynth may require a different driver.
## Use something like:
# fs.start(driver="pulseaudio")

sfid = fs.sfload("example.sf2")
fs.program_select(0, sfid, 0, 0)

for i in range(30, 90):
    fs.noteon(0, i, 30)
    print(i)
    time.sleep(.25)
    fs.noteoff(0, i)


time.sleep(1.0)

fs.delete()
