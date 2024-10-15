function [cancelled,adap,fit,P]=ARLS_N(primary,reference,order,lambd)
N=size(reference,2);%number of ref signals
 n=min(length(primary),length(reference));
 delayed=zeros(order,N);
 adap=zeros(order,N);
 I = eye(order*N);
 Delta=1e2;
P = I*Delta;
 for k = 1:n
    delayed(1,:) = reference(k,:);
    fit(k) = trace(delayed'*adap);
    cancelled(k) = primary(k)-fit(k);
    K = P*delayed(:)/(lambd+delayed(:)'*P*delayed(:));
    P = (I-K*delayed(:)')*P/lambd;
    adap = adap + cancelled(k)*reshape(K,order,N);
    delayed(2:order,:) = delayed(1:order-1,:);
end
end