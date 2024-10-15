   %****code edited (last 5 lines)****%
clc
clear all
close all
fs=10000;
f1=700;
t_duration=1;
t = 0:1/fs:t_duration-1/fs;
s = sin(2*pi*f1*t)+cos(8*pi*f1*t); %input signal
slen=length(s);
s=s';
[rn,c] = size(s);
d=0.000553239; %time delay in seconds
nfft = 2^nextpow2(2*slen); % To use max. computational efficiency of FFT
fax = fs*(-nfft/2:nfft/2-1)'/nfft; %  Create frequency shift vectors(bins)
      shft = exp(-j*d*2*pi*fax);   % w=2*pi*fax,, Frequency function for delay
      shft = ifftshift(shft);         % Make axis compatable with numeric FFT
      fsd = fft(s(:,1),nfft);        % Take FFT
      fsd = fsd.*shft;                %  Apply delay
      dum = ifft(fsd);                %  Return to time domain
      sd(:,1) = real(dum(1:slen));    %  Trim time domain signal to required length
s1=sin(2*pi*f1*(t-d))+cos(8*pi*f1*(t-d));
plot(s1);
hold on
plot(sd,'y');
legend('mathematically delayed','delayed in frequency domain');
diff=sd'-s1; %difference signal
stem(diff);