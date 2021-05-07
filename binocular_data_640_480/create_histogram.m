function p = create_histogram(data, n)
data_max = max(data);
data_min = min(data);
data_range = (data_max - data_min) / n;
p = zeros(1, n);
for i = 1:n
    p(i) = length(data(data > data_min + (i - 1) * data_range & data < data_min + i * data_range));
end
end
