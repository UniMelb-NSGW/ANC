gamma_a=0.01;
sigma_a=0.01;
D_a=1;
Nsim=100;
lambda=0.9999;
clear  scoreR01 scoreR02 scoreR03 scoreRg1 scoreRg2 scoreRg3 scoreR00 scoreRg0
for index =1:Nsim


	Nref=0;
	h=0.02;
	script;
	scoreRg0(index)=score_RLS1;
	h=0;
	script;
	scoreR00(index)=score_RLS1;

	Nref=1;
	order=15;
	h=0.02;
	script;
	scoreRg1(index)=score_RLS1;
	h=0;
	script;
	scoreR01(index)=score_RLS1;

	Nref=2;
	order=25;
	h=0.02;
	script;
	scoreRg2(index)=score_RLS1;
	h=0;
	script;
	scoreR02(index)=score_RLS1;
	Nref=9;
	h=0.02;
	order=40;
	script;
	scoreRg3(index)=score_RLS1;
	h=0;
	script;
	scoreR03(index)=score_RLS1;
	index
end
sth=[scoreR00 scoreR01 scoreR02 scoreR03 scoreRg0 scoreRg1 scoreRg2 scoreRg3];%
th=linspace(min(sth),max(sth),1001);
clear pfa_1 pfa_2 pfa_3 pd_1 pd_2 pd_3 pfa_0 pd_0
for n=1:1001
	pfa_0(n)=sum(scoreR00>th(n))/Nsim;
	pfa_1(n)=sum(scoreR01>th(n))/Nsim;
	pfa_2(n)=sum(scoreR02>th(n))/Nsim;
	pfa_3(n)=sum(scoreR03>th(n))/Nsim;

    pd_0(n)=sum(scoreRg0>th(n))/Nsim;
	pd_1(n)=sum(scoreRg1>th(n))/Nsim;
	pd_2(n)=sum(scoreRg2>th(n))/Nsim;
	pd_3(n)=sum(scoreRg3>th(n))/Nsim;
end
pfa=[pfa_0;pfa_1;pfa_2;pfa_3]';
pd=[pd_0;pd_1; pd_2;pd_3]';
plot(pfa,pd)