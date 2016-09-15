#This lets you visualize the printing for 4 channels that includes A, B and 2 other channels of your choosing
#The intention is for channel A to contain off-stoichiometric version of the target phase (elements 1 and 2) and channel B contains the under-represented element (element 2) and elements 3 and 4 are alloying elements
#concentration can be in any units as long as all values areconsistent
userinputd={\
'element_1': 'V', \
'element_2': 'Cu', \
'element_3': 'Cr', \
'element_4': 'W', \
'channel_element3': 'C', \
'channel_element4': 'H', \
'conc_el1_in_inkA': .57*.3, \
'conc_el2_in_inkA': .43*.3, \
'conc_el2_in_inkB': .4, \
'conc_el3': .03, \
'conc_el4': .03, \
'only_codes_with_alloys': True, \
}
