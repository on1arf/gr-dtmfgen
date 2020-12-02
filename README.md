# gr-dtmfgen
DTMF generator for GNU Radio  
  
This is the alpha test release of gr-dtmfgen, a embedded python block for generating DTMF message.
  
This block generates floats containing the frequencies of both DTMF tones.  
If this is fed to a VCO-block with sensitivity = 2 * n-p.pi, this creates the a sinewave at the required frequency  
This block also outputs 'volume-control' values that are be used to switch on/off the outputted sinewaves and their amplitude.  

The output of the lower tone is -2 db below the level of the higher tone.  
  
The python code itself is located inside the "DTMF generator" epy_block and as a seperate file "dtmf_generator.py".
  
The flowgraph "dtmfgen.grc" provides an example of an GRC flow that uses the gr-dtmfgen block.
