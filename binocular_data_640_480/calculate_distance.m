distance = zeros(1, 22);
variance = zeros(1, 22);
for x = 400:100:2500
    eval(['d', num2str(x), ' = abs((mm', num2str(x), '(:, 3) + mm', num2str(x), '(:, 1) - mm', num2str(x), '(:, 5) - mm', num2str(x), '(:, 7)) / 2);']); 
    eval(['distance(', num2str(x), '/100 - 3) = mean(d', num2str(x), ');']);
    eval(['variance(', num2str(x), '/100 - 3) = std(d', num2str(x), ')^2;']);
end
% variance = sort(variance,'descend');
% distance = sort(distance,'descend');
vFunc = polyfit(sort([400:100:2500]), sort(variance), 3);
% dFunc = @(beta, distance)beta(1)./distance + beta(2);
% beta = nlinfit(distance, [400:100:2500], dFunc, [9.2285e+04, 562.8836]);
dFunc = @(beta, distance)beta./distance;
beta = nlinfit(distance, [400:100:2500], dFunc, 700);
figure(1)
plot(distance, dFunc(beta, distance), 'r', distance, [400:100:2500], 'k');
figure(2)
plot(distance, vFunc(1).*(distance.^2) + vFunc(2).*(distance) + vFunc(3), 'r', distance, sqrt(variance), 'k');
clear x
