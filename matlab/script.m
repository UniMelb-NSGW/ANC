% clc; close all; clear all
W=1024; % sampling freq
N=655360;%2^14; 
T = N/W;
Nb = 64;
gamma = 1e-2; % std of GW freq
h = 0.025; % injected signal amp 
gamma_a = 1e-2; % frequency FM fluctuation in PEM
D_a=1;
sigma_a=0.01;
Nref=9;
% order = 15;
lambda = 0.9999;
% lambda=1;


f0=60; % center freq of ref
deltaf=0.1;
fq = cumsum([f0-deltaf gamma*sqrt(T)*randn([1 Nb-1])]);
H = 1; % noise of primary signal
Q = 1e-2; % noise of ref signal
ampr0 = 1;
ampr = 10;
% Nref=1;
[s,r,q,t,r0]=simulate_data_fft(f0,fq,h,H,W,N,Q,ampr0,ampr,gamma_a,D_a,sigma_a,Nref);
% [c2,a2,f2]=ARLS_N(s,r,18,lambda);%for 2 references
if Nref==0
	c1=s;
else
	[c1,a1,f1]=ARLS_N(s,r(:,1),order,lambda);%for 1 reference
end
%%
w=linspace(-W/2,W/2,N*Nb+1);w(end)=[];
% semilogy(w,fftshift([abs(fft(s));abs(fft(c2)); abs(fft(q))],2)','LineWidth',2)
% 
% grid on, axis tight, set(gca,'FontSize',14)
% xlim([58 62])
% xlabel('Frequency (Hz)')
% ylabel('FFT Spectrum')
% legend('Primary','ARLS','Signal')

%% HMM
% [sc, fh] = viterbi_for_ANC(gamma,q,N,Nb,T,W);
% c=s-r0;
% [score_0, fhat] = viterbi_for_ANC(gamma,c,N,Nb,T,W);
% [score_RLS2, fhat_RLS2] = viterbi_for_ANC(gamma,c2,N,Nb,T,W);
[score_RLS1, fhat_RLS1] = viterbi_for_ANC(gamma,c1,N,Nb,T,W);
%[score_RLS_100, fhat_RLS_100] = viterbi_for_ANC(gamma,c1,N,Nb,T,W);
% figure
% plot(t((N/2)+1:N:N*Nb+1),[fq],t((N/2)+1:N:N*Nb+1),fhat_RLS,'o-','LineWidth',2)
% legend('true','RLS')
% grid on, axis tight, set(gca,'FontSize',14)
% xlabel('Time')
% ylabel('Frequency (Hz)')
% figure
% plot(r0-f2)