clc; close all; clear all
f0 = 60; % center freq of ref
h = 0.03; % injected signal amp 
H = 1; % noise of primary signal
Q = 2; % noise of ref signal
gamma_a = 1e-1;
ampr0 = 1;
ampr = 10;
score_mat = []; % without filtering
%score_LMS_mat = [];
score_RLS_mat = [];
tic
for ind = 1:300
    if rand>0.5
        [score,score_RLS] = ANC_filter(h,f0,ampr0,ampr,H,Q,gamma_a);
        k_all(ind) = 1;
    else 
        [score,score_RLS] = ANC_filter(0,f0,ampr0,ampr,H,Q,gamma_a);
        k_all(ind) = 0;
    end
score_mat = [score_mat score];
%score_LMS_mat = [score_LMS_mat score_LMS];    
score_RLS_mat = [score_RLS_mat score_RLS];
end
toc

th_nofilter = linspace(min(score_mat),max(score_mat),1001);
%th_LMS = linspace(min(score_LMS_mat),max(score_LMS_mat),1001);
th_RLS = linspace(min(score_RLS_mat),max(score_RLS_mat),1001);
for i=1:1001
    pd_nofilter(i)=sum(score_mat(k_all==1)>=th_nofilter(i));
    pf_nofilter(i)=sum(score_mat(k_all==0)>=th_nofilter(i));
    %pd_LMS(i)=sum(score_LMS_mat(k_all==1)>=th_LMS(i));
    %pf_LMS(i)=sum(score_LMS_mat(k_all==0)>=th_LMS(i));
    pd_RLS(i)=sum(score_RLS_mat(k_all==1)>=th_RLS(i));
    pf_RLS(i)=sum(score_RLS_mat(k_all==0)>=th_RLS(i));
end
pd_nofilter=pd_nofilter/sum(k_all==1);
pf_nofilter=pf_nofilter/sum(k_all==0);
%pd_LMS=pd_LMS/sum(k_all==1);
%pf_LMS=pf_LMS/sum(k_all==0);
pd_RLS=pd_RLS/sum(k_all==1);
pf_RLS=pf_RLS/sum(k_all==0);
roc=[pd_nofilter;pf_nofilter;pd_RLS;pf_RLS]';
% %% plot roc
% figure
% semilogx(points_vit(2,:),points_vit(1,:),'LineWidth',2)
% hold on
% semilogx(points_vit(4,:),points_vit(3,:),'LineWidth',2)
% legend('without filtering','RLS','FontSize',16)
% %%
% figure
% subplot(311)
% semilogx(points0055(2,:),points0055(1,:),'LineWidth',2)
% title('h=0.055')
% hold on
% %semilogx(pf_LMS,pd_LMS,'o-')
% semilogx(points0055(4,:),points0055(3,:),'LineWidth',2)
% legend('without filtering','RLS','FontSize',16)
% axis tight; grid on; xlabel('pfa'); ylabel('pd');
% subplot(312)
% semilogx(points006(2,:),points006(1,:),'LineWidth',2)
% hold on
% title('h=0.06')
% %semilogx(pf_LMS,pd_LMS,'o-')
% semilogx(points006(4,:),points006(3,:),'LineWidth',2)
% legend('without filtering','RLS','FontSize',16)
% axis tight; grid on; xlabel('pfa'); ylabel('pd');
% subplot(313)
% semilogx(points0076(2,:),points0076(1,:),'LineWidth',2)
% hold on
% title('h=0.076')
% %semilogx(pf_LMS,pd_LMS,'o-')
% semilogx(points0076(4,:),points0076(3,:),'LineWidth',2)
% legend('without filtering','RLS','FontSize',16)
% axis tight; grid on; xlabel('pfa'); ylabel('pd');