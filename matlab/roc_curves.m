gamma_a=0.01;
sigma_a=0.01;
D_a=1;
Nsim=100;
clear  scoreR0 scoreRg
for index =1:Nsim
	h=0.022;
	script;
	scoreRg(index)=score_RLS1;
	h=0;
	script;
	scoreR0(index)=score_RLS1;
	index
end
sth=[scoreR0  scoreRg];%
th=linspace(min(sth),max(sth),1001);
clear pfa_1 pfa_2 pfa_3 pd_1 pd_2 pd_3
for n=1:1001
	pfa(n)=sum(scoreR0>th(n))/Nsim;
	pd(n)=sum(scoreRg>th(n))/Nsim;
end
plot(pfa,pd)