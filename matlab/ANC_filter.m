function [score,score_RLS] = ANC_filter(h,f0,ampr0,ampr,H,Q,gamma_a)
% par h: amp of injected signal, f0: powere line freq

W=1000; % sampling freq
N=2^14; 
T = N/W;
Nb = 50;
gamma = 1e-2; % std of GW freq
%fq = 59.995+gamma*randn([1 Nb]); % GW freq
fq = cumsum([59.5 gamma*sqrt(T)*randn([1 Nb-1])]);
%f0 = 60; % center freq of ref
%h = 2; % injected signal amp 
%H = 1; % noise of primary signal
%Q = 1; % noise of ref signal
%ampr0 = 1;
%ampr = 1;
[s,r,~,~,~]=simulate_data(f0,fq,h,H,W,N,Q,ampr0,ampr,gamma_a);
%order = 10;
lambda = 1;
%[c_LMS,~,~]=ALMS_N(s,r,order); % [cancelled,adap,fit]
[c_RLS,~,~]=ARLS_N(s,r,36,lambda);
[score, ~] = viterbi_for_ANC(gamma,s,N,Nb,T,W);
%[score_LMS, ~] = viterbi_for_ANC(gamma,c_LMS,N,Nb,T,W);
[score_RLS, ~] = viterbi_for_ANC(gamma,c_RLS,N,Nb,T,W);
end