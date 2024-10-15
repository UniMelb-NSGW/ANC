function [s,R,q,t,r0]=simulate_data_fft(f0,fq,h,H,W,N,Q,ampr0,ampr,gamma_a,D_a,sigma_a,NumRef)
% gamma_a: phase fluctuation
%s=r0+q+noise: primary
%r =amplr*r0+time/phase shift: reference
%q injected
% SNR:  h/(H) 
%f0=50;% 
NT=length(fq);
% t=repmat((0:N-1)/W,1,NT); % NT: number of blocks
dt=1/W;
t=(0:(N*NT-1))/W;
taug=(0:(N*NT+100))/W;
T=N/W; % time within one block
mag0=(rand(1,length(t))-0.5)/10+ampr0;
phase=2*pi*f0*taug+2*pi*D_a*cos(2*pi*gamma_a*taug)+randn(1,length(taug))*sigma_a;
S=sin(phase);
r0 = mag0.*S(1:length(t));
%
t0=rand(3,1)*dt*10; %random time delay (max three)
%tree phases
tdelta=[0 1/3/f0 2/3/f0];
tdel=t0'+tdelta';
tdel=tdel(:);
R=[];
for n=1:NumRef
	mag=(rand(1,length(t))-0.5)/10+ampr; % magnitude noise
	S_delayed=delay_sig(S,dt,tdel(n));
	r=mag.*S_delayed(1:length(t))+randn(1,length(t))*Q;
	R(:,n)=r.';
end
% r=simulate_references(gamma_a,t,NumRef,f0,ampr/ampr0*mag,Q);
p=point_phase(fq,t(1:N),T);
q=h*sin(2*pi*p);% h can be random
if NumRef==0
	r0=0;
end
s = r0+q+randn(1,length(t))*H;
