function [IFmset IA smset sDif] = VNCMD2_2(s,fs,eIF,alpha,beta,var,tol)
% Variational Nonlinear Chirp Mode Decomposition (VNCMD)
% Authors: Shiqian Chen and Zhike Peng
% mailto:chenshiqian@sjtu.edu.cn; z.peng@sjtu.edu.cn;
% https://www.researchgate.net/profile/Shiqian_Chen2   https://www.researchgate.net/profile/Z_Peng2
%
%%%%%%%%%%%%%%%%%%%%%%%  input %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% s: measured signal,a row vector
% fs: sampling frequency
% eIF: initial instantaneous frequency (IF) time series for all the signal modes; each row of eIF corresponds to the IF of each mode
% alpha: penalty parameter controling the filtering bandwidth of VNCMD;the smaller the alpha is, the narrower the bandwidth would be
% beta: penalty parameter controling the smooth degree of the IF increment during iterations;the smaller the beta is, the more smooth the IF increment would be
% var: the variance of the Gaussian white noise; if we set var to zero, the noise variable u (see the following code) will be dropped.
% tol: tolerance of convergence criterion; typically 1e-7, 1e-8, 1e-9...
%%%%%%%%%%%%%%%%%%%%%%% output %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% IFmset: the collection of the obtained IF time series of all the signal modes at each iteration
% smset: the collection of the obtained signal modes at each iteration
% IA: the finally estimated instantaneous amplitudes of the obtained signal modes

% When using this code, please do cite our papers:
% -----------------------------------------------
% Chen S, Dong X, Peng Z, et al, Nonlinear Chirp Mode Decomposition: A Variational Method, IEEE Transactions on Signal Processing, 2017.
% Chen S, Peng Z, Yang Y, et al, Intrinsic chirp component decomposition by using Fourier Series representation, Signal Processing, 2017.
% Chen S, Dong X, Xing G, et al, Separation of Overlapped Non-Stationary Signals by Ridge Path Regrouping and Intrinsic Chirp Component Decomposition, IEEE Sensors Journal, 2017.
%% initialize
[K,N] = size(eIF);%K is the number of the components£¬N is thenumber of the samples
t = (0:N-1)/fs;%time
e = ones(N,1);
e2 = -2*e;
% e2(1) = -1;e2(end) = -1;
oper = spdiags([e e2 e], 0:2, N-2, N);% oper = spdiags([e e2 e], -1:1, N, N);%the modified second-order difference matrix
opedoub = oper'*oper;%
sinm = zeros(K,N);cosm = zeros(K,N);%
xm = zeros(K,N);ym = zeros(K,N);%denote the two demodulated quadrature signals
iternum = 300; %the maximum allowable iterations

%%%%%%%%%%%%%%%%%%% adjust initial IF time series
wb=[];wh=[];f_re=[];
f_re=eIF(4,:);lc_r=4;
for i=K-1:K
    if ~isempty(find(eIF(i,:)<0))
        f_re=eIF(i,:);lc_r=i;
    end
end
wb=eIF(1,:);lc_b=1;
wh=eIF(2,:);lc_h=2;
if mean(eIF(2,:))<1
    [va,vb]=max(mean(eIF(2:3,:),2));
    wh=eIF(vb+1,:);
    lc_h=vb+1;
end
nn=[1:K];
lc_m=find(nn~=lc_b&nn~=lc_h&nn~=lc_r);
lc=[lc_b,lc_h,lc_m];
fh=mean(wh(1,:));
fb=mean(wb(1,:));
A=[];b=[];Aeq=[]; beq=[];

for i=1:N
vlb=[0.01;1;0.5;0.7;-5;0.7];
vub=[0.8;2.5;4;1.5;5;1.5];
k=wb(i)/fb;
n=wh(i)/fh;
x0=[fb,fh,k,n,1,1];
tic;
option=optimset('LargeScale','off','display','off');
[gama,fval]=fmincon(@(x)optf(x,eIF(lc,i)),x0,A,b,Aeq,beq,vlb,vub,@(x)noncon(x,eIF(lc,i)),option);
toc
eIF(:,i)=[gama(1);gama(2);gama(5)*gama(1)+gama(6)*gama(2);f_re(i)];
end
beta = 1e-5;
eIF = curvesmooth(eIF,beta); 
% figure;
% plot(t,eIF,'linewidth',3); % initial IFs
% title('adjusted iniIF');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
IFsetiter = zeros(K,N,iternum+1); IFsetiter(:,:,1) = eIF; %the collection of the obtained IF time series of all the signal modes at each iteration
ssetiter = zeros(K,N,iternum+1); %the collection of the obtained signal modes at each iteration
lamuda = zeros(1,N);%Lagrangian multiplier
for i = 1:K
    sinm(i,:) = sin(2*pi*(cumtrapz(t,eIF(i,:))));
    cosm(i,:) = cos(2*pi*(cumtrapz(t,eIF(i,:))));
    Bm = spdiags(sinm(i,:)', 0, N, N);Bdoubm = spdiags((sinm(i,:).^2)', 0, N, N);%Bdoubm = Bm'*Bm
    Am = spdiags(cosm(i,:)', 0, N, N);Adoubm = spdiags((cosm(i,:).^2)', 0, N, N);%Adoubm = Am'*Am
    xm(i,:) = (2/alpha*opedoub + Adoubm)\(Am'*s(:));
    ym(i,:) = (2/alpha*opedoub + Bdoubm)\(Bm'*s(:));
    ssetiter(i,:,1) = xm(i,:).*cosm(i,:) + ym(i,:).*sinm(i,:);%
end
%% iterations 
iter = 1;% iteration counter
% sDif = tol + 1;%
sDif=zeros(1,iternum+1);
sDif(1)=tol+1;
sum_x = sum(xm.*cosm,1);%cumulative sum
sum_y = sum(ym.*sinm,1);%cumulative sum
% while ( sDif > tol &&  iter <= iternum ) % 
while ( sDif(iter) > tol &&  iter <= iternum && isempty(find(eIF(1,:)<0|eIF(1,:)>0.8))&& isempty(find(eIF(2,:)<1|eIF(2,:)>2.2))) % 
   
    betathr = 10^(iter/36-10);%gradually increase the parameter beta during the iterations
    if betathr>beta
        betathr = beta; 
    end
    
    u = projec(s - sum_x - sum_y - lamuda/alpha,var);%projection operation; u denotes the noise variable; if let var=0, the output u will be zeros. 
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%  update each mode  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
    for i = 1:K
        
       % lamuda = zeros(1,N);% if one wants to drop the Lagrangian multiplier, just set it to zeros, i.e., delete the first symbol % in this line.
       
%%%%%%%%%%%%% update the two matrices A and B %%%%%%%%%%%%%%%%%%%%%%%%%%%         
       Bm = spdiags(sinm(i,:)', 0, N, N);Bdoubm = spdiags((sinm(i,:).^2)', 0, N, N);
       Am = spdiags(cosm(i,:)', 0, N, N);Adoubm = spdiags((cosm(i,:).^2)', 0, N, N);
%%%%%%%%%%%%% x-update %%%%%%%%%%%%%%%%%%%%%%%%%%%
       sum_x = sum_x - xm(i,:).*cosm(i,:);% remove the relevant component from the sum
       xm(i,:) = (2/alpha*opedoub + Adoubm)\(Am'* (s - sum_x - sum_y - u - lamuda/alpha)');%
       interx = xm(i,:).*cosm(i,:);% temp variable
       sum_x = sum_x + interx;% update the sum
%%%%%%%%%%%%% y-update %%%%%%%%%%%%%%%%%%%%%%%%%%%
       sum_y = sum_y - ym(i,:).*sinm(i,:);% remove the relevant component from the sum
       ym(i,:) = (2/alpha*opedoub + Bdoubm)\(Bm'* (s - sum_x - sum_y - u - lamuda/alpha)');
%%%%%%%%%%%%%  update the IFs  %%%%%%%%%%%%%%%%%%%%%%%%       
       ybar = Differ(ym(i,:),1/fs); xbar = Differ(xm(i,:),1/fs);%compute the derivative of the functions
       deltaIF = (xm(i,:).*ybar - ym(i,:).*xbar)./(xm(i,:).^2 + ym(i,:).^2)/2/pi;% obtain the frequency increment by arctangent demodulation
       deltaIF = (2/betathr*opedoub + speye(N))\deltaIF';% smooth the frequency increment by low pass filtering
%        eIF(i,:) = eIF(i,:) - 0.5*deltaIF';% update the IF
       eIF(i,:) = eIF(i,:) - 0.025*deltaIF';% update the IF
%%%%%%%%%%%%%  update cos and sin functions  %%%%%%%%%%%%%%%%%%%%%%%%          
       sinm(i,:) = sin(2*pi*(cumtrapz(t,eIF(i,:))));
       cosm(i,:) = cos(2*pi*(cumtrapz(t,eIF(i,:))));
%%%%%%%%%%%%% update sums %%%%%%%%%%%%%%%%%       
       sum_x = sum_x - interx + xm(i,:).*cosm(i,:); %
       sum_y = sum_y + ym(i,:).*sinm(i,:);%
       ssetiter(i,:,iter+1) = xm(i,:).*cosm(i,:) + ym(i,:).*sinm(i,:);%
    end
    IFsetiter(:,:,iter+1) = eIF;
    
%%%%%%%%%%%%% update Lagrangian multiplier %%%%%%%%%%%%%%%%%     
lamuda = lamuda + alpha*(u + sum_x + sum_y -s);

%%%%%%%%%%%%%%%%%%%%%%%%%%% restart scheme %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
if norm(u + sum_x + sum_y -s)>norm(s) %
   lamuda = zeros(1,length(t));
   for i = 1:K
    Bm = spdiags(sinm(i,:)', 0, N, N);Bdoubm = spdiags((sinm(i,:).^2)', 0, N, N);%
    Am = spdiags(cosm(i,:)', 0, N, N);Adoubm = spdiags((cosm(i,:).^2)', 0, N, N);%
    xm(i,:) = (2/alpha*opedoub + Adoubm)\(Am'*s(:));
    ym(i,:) = (2/alpha*opedoub + Bdoubm)\(Bm'*s(:));
    ssetiter(i,:,iter+1) = xm(i,:).*cosm(i,:) + ym(i,:).*sinm(i,:);
   end
   sum_x = sum(xm.*cosm,1);%
   sum_y = sum(ym.*sinm,1);%
end

%%%%%%%%%%%%%  compute the convergence index %%%%%%%%%%%%%%%%%%  
%     sDif = 0;
%     for i = 1:K
%         sDif = sDif + (norm(ssetiter(i,:,iter+1) - ssetiter(i,:,iter))/norm(ssetiter(i,:,iter))).^2;
%     end
%     iter = iter + 1;

    for i = 1:K
        sDif(iter+1) = sDif(iter+1) + (norm(ssetiter(i,:,iter+1) - ssetiter(i,:,iter))/norm(ssetiter(i,:,iter))).^2;
    end
    iter = iter + 1;
end
    IFmset = IFsetiter(:,:,1:iter);
    smset = ssetiter(:,:,1:iter);
    IA = sqrt(xm.^2 + ym.^2);
end
    
function y=optf(x,a)
 B=[0,0,1,0,1,0;
    0,0,0,1,0,1;
    1,0,0,0,0,0;
    0,1,0,0,0,0; 
    1,0,0,0,0,0;
    0,1,0,0,0,0];
y=sum(a)-0.5*x*B*x';
end
function [yc yceq]=noncon(x,a,idx)
% function [yc yceq]=noncon(x,a)
yc=[];
yceq=[];
yc=[yc;-(x(3)*x(1)-x(4)*x(2))^2];      %% Ax < b
yc=[yc;-(x(3)*x(1)-x(5)*x(1)-x(6)*x(2))^2]; 
yc=[yc;-(x(4)*x(2)-x(5)*x(1)-x(6)*x(2))^2]; 

% yceq=[yceq;prod(x(3)*x(1)-a)];
% yceq=[yceq;prod(x(4)*x(2)-a)];
% yceq=[yceq;prod(x(5)*x(1)+x(6)*x(2)-a)];
yceq=[yceq;x(3)*x(1)-a(1)];
yceq=[yceq;x(4)*x(2)-a(2)];
yceq=[yceq;x(5)*x(1)+x(6)*x(2)-a(3)];
end