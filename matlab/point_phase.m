function p=point_phase(f,t,T)

df=diff(f)/T;
df(end+1)=0;
p=[];
pn=0;
for n=1:length(f)
	p=[p pn+f(n)*t+df(n)*t.^2/2];
	pn=pn+f(n)*T+df(n)*T.^2/2;
end
