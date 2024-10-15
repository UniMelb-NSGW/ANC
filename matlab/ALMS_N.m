function [cancelled,adap,fit]=ALMS_N(primary,reference,order)
% primary --- signal+line
% reference ---  line only
%order - fliter order
%cancelled ---  signal with line cancelled
if nargin==2
 order=2;
end
 mu=1e-4;
 N=size(reference,2);
 n=min(length(primary),length(reference));
 delayed=zeros(N,order);
 adap=zeros(N,order);
 cancelled=zeros(1,n);
 fit=zeros(1,n);
 for k=1:n
     delayed(:,1)=reference(k,:)';
	 fit(k)=trace(delayed*adap');
     cancelled(k)=primary(k)-fit(k);
	 adap = adap + 2*mu*cancelled(k) * delayed;
     delayed(:,2:order)=delayed(:,1:order-1);
 end
