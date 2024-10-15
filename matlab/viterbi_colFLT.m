function [path,delta,score,psi,stat] = viterbi_colFLT(M, obslik)
% VITERBI Find the most-probable (Viterbi) path through the HMM state trellis.
% path = viterbi(prior, transmat, obslik)
%
% Inputs:
% transmat(i,j) = Pr(Q(t+1)=j | Q(t)=i)
% O - measurements
%
% Outputs:
% path(t) = q(t), where q1 ... qT is the argmax of the above expression.
% delta(j,t) = prob. of the best sequence of length t-1 and then going to state j, and O(1:t)
% psi(j,t) = the best predecessor state, given that we ended up in state j at t
% tic
% if round(M/2)==M/2 M=M+1;end
[Q,T]=size(obslik);


delta = zeros(Q,T);
psi = zeros(Q,T);
path = zeros(1,T);
       
t=1;
delta(:,t) = obslik(:,t);
cor=(0:Q-1)'-ceil((M-1)/2);% correction term
% disp('forward')
for t=2:T
  delta(:,t)= colfilt(delta(:,t-1),[M 1],'sliding',@max)+obslik(:,t);
  psi(:,t)  = colfilt(delta(:,t-1),[M 1],'sliding',@argmax)+cor;
end
%sort the paths
% disp('backward')
% D=10;
% maxtab=peakdet(delta(:,T),D);
% [s,n]=sort(maxtab(:,2),'descend');
% ind=round(maxtab(n,1));
% Nind=length(ind);
Nind=1;
[score,ind]=max(delta(:,T));
k=[1:ind-T ind+T:Q];
for n=1:Nind
    [path(n,T)] = ind(n);
    for t=T-1:-1:1
        path(n,t) = psi(path(n,t+1),t+1);
    end
end
% toc