function u = projec(vec,var)
%projection operation
%vec: the vector for projection
%var: the variance of the noise
M = length(vec);%
e = sqrt(M*var);%upper bound determined by the noise level
 u = vec;
if norm(vec) > e
    u = e/norm(vec)*vec;
end
end