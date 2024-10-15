%this computes viterbi path of frequencies, given the data Y1
% parameters, like gamma and N are the same as in MCMC
% divide frequency into the bins
function [score, fhat,y0] = viterbi_for_ANC(gamma,Y1,N,Nblocks,T,W)
w=linspace(-W/2,W/2,2*N+1);w(end)=[];
% [~,k]=min(abs(w-60));

dw=w(2)-w(1);% frequency bin
% do fft for each block of Y1
y=abs(fftshift(fft(reshape(Y1,N,Nblocks),2*N),1)); %N
% y0=y(k+[-250:250],:);
% y0=y(N+1:2*N,:);
n=find(abs(w-60)<10);
w0=w(n);
y0=y(n,:);
% figure out how far (in bins) the  frequency wanders over 1 block, making sure that M>=1
%M=max(1,ceil(sqrt(3)*sqrt(N*1e-2)*gamma/dw));
M=max(1,ceil(2*sqrt(T)*gamma/dw))
%compute Viterbi path
[path,delta] = viterbi_colFLT(2*M+1, y0);
score=max(delta(:,end))-mean(delta(:,end));
% w0=w(N+1:2*N);
% w0=w(k+[-250:250]);
fhat = w0([path]);
end
%plot the result
% plot(1:L+1,f_ori,(N/2)+1:N:L+1,w([path]),'o-','LineWidth',2)