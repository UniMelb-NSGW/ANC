function [R]=simulate_references(gamma_a,time,N,f0,ampr,Q)
%t- time
%N-how many measurements
%R- references
%f0=50;% 
dt=time(2)-time(1);
t0=rand*dt*10; %random time delay
%tree phases
tdelta=[0 1/3/f0 2/3/f0];
for n=1:N
	mag=rand(1,length(time))/100+ampr; % magnitude noise
	a=cos(2*pi*gamma_a*(time+t0+tdelta(n)))+randn(1,length(time))/100;
	r=mag.*sin(2*pi*(f0*(time+t0+tdelta(n))+a))+randn(size(time))*Q;
	R(:,n)=r.';
end
