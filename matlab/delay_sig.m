function s=delay_sig(s0,dt,d)
%
slen=length(s0);
W=1/dt;
nfft = 2^nextpow2(2*slen);
fax = W*(-nfft/2:nfft/2-1)/nfft; 
shft = exp(j*d*2*pi*fax);   % w=2*pi*fax,, Frequency function for delay
shft = ifftshift(shft);         % Make axis compatable with numeric FFT
fsd = fft(s0,nfft);        % Take FFT
fsd = fsd.*shft;                %  Apply delay
dum = ifft(fsd);                %  Return to time domain
s = real(dum(1:slen));    %  Trim time domain signal to required length