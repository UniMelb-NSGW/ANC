E=G0.Edges.EndNodes;
b=G0.Edges.Weight;
e=unique(E(:));
E=[0 1;E; 9 0];
M=size(E,1);
N=length(e);
A0=zeros(N,M);
f=zeros(M,1);
f(E(:,2)==n)=1;
for n=1:N
	   %flow in
       k=find(E(:,2)==n); 
	   A0(n,k)=-1;
	   %flow out
	   m=find(E(:,1)==n);
	   A0(n,m)=1;
end
A=eye(M);A([1 M],:)=[];
lb=zeros(M,1);
options = optimoptions(@linprog,'Algorithm','dual-simplex','Display','none');
x=linprog(-f,A,b,A0,b0,lb,[],options);