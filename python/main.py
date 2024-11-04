

# This should be a jupyer notebook, but putting it here for now just to get basic structure in place



sampling_frequency = 1024 # Hz
N = 2**14                 #todo, what is this value and where does it come from?. From the definition of T, it looks like the total number of samples?

T = N/sampling_frequency # Total time of data




γ = 1e-2 # std of GW freq



Nb = 64

h = 0.025 # amplitude of the injected GW signal

γa = 1e-2 

f = 60 # Hz. Central frequency
Δf = 1.0 # Hz
sigma_a=0.01



#Parameters of the reference signal


#Parameters of the injected GW


#Parameters of the filter
Nref=9

order = 15 # order of the filter


λ = 0.9999 #forgetting factor



f0=60; % center freq of ref
deltaf=0.1;
fq = cumsum([f0-deltaf γ*sqrt(T)*randn([1 Nb-1])]);







H = 1; % noise of primary signal
Q = 1e-2; % noise of ref signal
ampr0 = 1;
ampr = 10;

[s,r,q,t,r0]=simulate_data_fft(f0,fq,h,H,W,N,Q,ampr0,ampr,gamma_a,D_a,sigma_a,Nref);



if Nref==0
	c1=s
else
	[c1,a1,f1]=ARLS_N(s,r(:,1),order,lambda);%for 1 reference
end







%% HMM
[score_RLS1, fhat_RLS1] = viterbi_for_ANC(gamma,c1,N,Nb,T,W);
