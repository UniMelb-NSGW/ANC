W=1000; % sampling freq
N=2^14; 
T = N/W;
Nb = 50;
gamma = 1e-2; % std of GW freq
gamma_a = 2e-2; % frequency FM fluctuation in PEM
f0=60; % center freq of ref

h = 0.025; % injected signal amp 
H = 1; % noise of primary signal
Q = 0.01; % noise of ref signal
ampr0 = 1.2;
ampr = 10;
% L1=zeros(1,30);
% L2=zeros(1,30);
% L3=zeros(1,30);
% L=zeros(1,10);
for index=11:100
	fq = cumsum([60 gamma*sqrt(T)*randn([1 Nb-1])]);
	[s,r,q,t,r0]=simulate_data(f0,fq,h,H,W,N,Q,ampr0,ampr,gamma_a);
	lambda = 1;
    c=s-r0;
	[score, fhat] = viterbi_for_ANC(gamma,c,N,Nb,T,W);
	L(index)=sqrt(mean((fq-fhat).^2))
	for m=11:30
		[c1,a1,f1]=ARLS_N(s,r(:,1),m,1);
		[score_RLS1, fhat_RLS1] = viterbi_for_ANC(gamma,c1,N,Nb,T,W);
		L1(m)=L1(m)+sqrt(mean((fq-fhat_RLS1).^2));
		[c2,a2,f2]=ARLS_N(s,r(:,1:2),m,1);
		[score_RLS2, fhat_RLS2] = viterbi_for_ANC(gamma,c2,N,Nb,T,W);
		L2(m)=L2(m)+sqrt(mean((fq-fhat_RLS2).^2));
		[c3,a3,f3]=ARLS_N(s,r,m,1);
		[score_RLS3, fhat_RLS3] = viterbi_for_ANC(gamma,c3,N,Nb,T,W);
		L3(m)=L3(m)+sqrt(mean((fq-fhat_RLS3).^2));
	end
	disp(index)
	plot([L1/index;L2/index;L3/index]'), title(num2str(index)), drawnow
end