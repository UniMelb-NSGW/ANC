function [s,R,q,t,r0]=simulate_data(f0,fq,h,H,W,N,Q,ampr0,ampr,gamma_a,D_a,sigma_a)
% gamma_a: phase fluctuation
%s=r0+q+noise: primary
%r =amplr*r0+time/phase shift: reference
%q injected
% SNR:  h/(H) 
%f0=50;% 
NT=length(fq);
% t=repmat((0:N-1)/W,1,NT); % NT: number of blocks
dt=1/W;
t0=rand*dt*10; %random time delay
t=(0:(N*NT-1))/W;
taug=(0:(N*NT+100))/W;
T=N/W; % time within one block
mag0=rand(1,length(t))/1000+ampr0;
phase=2*pi*f0*t+2*pi*D_a*cos(2*pi*gamma_a*t);
noise=randn(1,length(taug))*sigma_a;
r0 = mag0.*sin(phase+noise(1:length(t)));
NumRef = 1;
%tree phases
tdelta=[0 1/3/f0 2/3/f0];
for n=1:NumRef
	mag=rand(1,length(t))/100+ampr; % magnitude noise
	tt=t+t0+tdelta(n);
	phase_delayed=2*pi*f0*tt+2*pi*D_a*cos(2*pi*gamma_a*tt);
	noise_delayed=delay_sig(noise,dt,t0+tdelta(n));
	phase_delayed=phase_delayed+noise_delayed(1:length(t));
% 	
	r=mag.*sin(phase_delayed)+randn(1,length(t))*Q;
	R(:,n)=r.';
end
% r=simulate_references(gamma_a,t,NumRef,f0,ampr/ampr0*mag,Q);
p=point_phase(fq,t(1:N),T);
q=h*sin(2*pi*p);% h can be random
s = r0+q+randn(1,length(t))*H;
