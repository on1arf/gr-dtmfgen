"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!


"""
#gr-dtmfgen: a gnuradio embedded python block for generationg DTMF messages
#--------------------------------------------------------------------------
#
#
#This is the alpha test release of gr-dtmfgen, a embedded python block for generating
#DTMF message.
#
#
# this block generates floats containing the frequencies of both DTMF tones
# if this is fed to a VCO-block with sensitivity = 2 * n-p.pi, this creates the a sinewave at the required frequency
# this block also outputs 'volume-control' values that are be used to switch on/off the outputted sinewaves and
# their amplitude
# the output of the lower tone is -2 db below the level of the higher tone
#
#
#The python code itself is located inside the "DTMF generator" epy_block and as a seperate file "gr-dtmf_generator.py".
#
#
# (C) Kristoff Bonne, ON1ARF
# GPL v3
#
#Release-information:
#Version: 0.0.1 (20201129)
#
# 73s . kristoff - ON1ARF


import numpy as np
from gnuradio import gr

import time



class pdtmf_generator(gr.sync_block):

	# init some data
	freqtable=((697.0,770.0,852.0,941.0,1209.0,1336.0,1477.0,1633.0))
	char2freq={
		'1':(0,4), '2':(0,5), '3':(0,6), 'A':(0,7),
		'4':(1,4), '5':(1,5), '6':(1,6) ,'B':(1,7),
		'7':(2,4), '8':(2,5), '9':(2,6), 'C':(2,7),
		'*':(3,4), '0':(3,5), '#':(3,6), 'D':(3,7)
		}

	amplitude=(10**(-0.2),1.0) #lower tone is 2 db below higher tone 




	def __init__(self, txt = '123456', ontime=5,  offtime=1, sleeptime= 30):  # only default arguments here
		gr.sync_block.__init__(
			self,
			name='dtmf generator',
			in_sig=[],
			out_sig=[np.float32,np.float32,np.float32,np.float32]
		)


		# convert to integers
		try:
			ontime,offtime,sleeptime=(int(ontime),int(offtime),int(sleeptime))
		except ValueError:
			raise ValueError("Error converting ontime, offtime or sleeptime to integers")

		# checking input
		if ontime < 0: raise ValueError("Error: on-time can not be negative")
		if offtime < 0: raise ValueError("Error: off-time can not be negative")
		if sleeptime < 0: raise ValueError("Error: sleep-time can not be negative")

		# make text uppercase
		txt=txt.upper()

		# create dtmg message
		dtmfmessage=[]

		for c in txt:
			try:
				f1,f2=pdtmf_generator.char2freq[c]
			except KeyError:
				# unknown character -> ignore it
				continue
			#endtry

			# DTMF message is DTMF tones + silence
			dtmfmessage+=[(pdtmf_generator.freqtable[f1],pdtmf_generator.amplitude[0],pdtmf_generator.freqtable[f2],pdtmf_generator.amplitude[1]) for _ in range(ontime)] + [(0.0,0.0,0.0,0.0) for _ in range(offtime)]
		#end for


		# do we have a valid message?
		l=len(dtmfmessage)
		if l == 0: raise ValueError("No valid text to send")


		# the message is OK!

		# add 'sleeptime' periodes of silence
		dtmfmessage += [(0.0,0.0,0.0,0.0) for _ in range(sleeptime)]

		self.set_output_multiple(l+sleeptime)

		self.dtmfmessage=list(zip(*dtmfmessage))
		self.msglen=l+sleeptime

	#end __init__

	def work(self, input_items, output_items):
		# copy DTMS message-data for all 4 output channels
		for i in range(4):
			output_items[i][:self.msglen]=np.array(self.dtmfmessage[i], dtype=np.float32)
		#end for

		return self.msglen # done

	#end work
# end class "pdtmf_generator"
