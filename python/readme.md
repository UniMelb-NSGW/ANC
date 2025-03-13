Note of  any differences between matlab and Python



* delay_sig in matlab defines the frequency function for delay  as `shft = exp(j*d*2*pi*fax);   % w=2*pi*fax`. In Python the exponent has a negative sign. But I think the actually advances the signal; In Python we use the negative exponential
