
for index =1:100
	h=0.025;
    D_a=0.1;
	script;
	scoreRg1(index)=score_RLS1;
	D_a=0.25;
	script;
	scoreRg2(index)=score_RLS1;
    D_a=0.5;
	script;
	scoreRg3(index)=score_RLS1;
    h=0;
	script;
	scoreR0(index)=score_RLS1;
	index
end
sth=[scoreR0 scoreRg1 scoreRg2 scoreRg3];%scoreR02 score0 scoreRH1 scoreRH2 scoreH];
th=linspace(min(sth),max(sth),1001);
for n=1:1001
	pfa(n)=sum(scoreR0>th(n))/100;
	pd_1(n)=sum(scoreRg1>th(n))/100;
	pd_2(n)=sum(scoreRg2>th(n))/100;
	pd_3(n)=sum(scoreRg3>th(n))/100;
end
pd=[pd_1; pd_2;pd_3];
plot(pfa,pd)