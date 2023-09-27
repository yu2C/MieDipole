% Define the range of real values for z
z_values = linspace(0, 14, 1000);

% Initialize arrays for rcy values for different n values
n_values = [1, 2, 3];
rcy_values = zeros(length(n_values), length(z_values));

% Calculate rcy for each n and each real value of z
for i = 1:length(n_values)
    n = n_values(i);
    for j = 1:length(z_values)
        z = z_values(j);
        [~, rcy, ~, ~] = rcbesselc(z, n);
        rcy_values(i, j) = rcy(n + 1);  % MATLAB uses 1-based indexing
    end
end

% Plot rcy for different n values as a function of the real part of z
figure;
plot(z_values, real(rcy_values(1, :)), 'b', 'LineWidth', 1.5, 'DisplayName', 'rcy, n=1');
hold on;
plot(z_values, real(rcy_values(2, :)), 'r', 'LineWidth', 1.5, 'DisplayName', 'rcy, n=2');
plot(z_values, real(rcy_values(3, :)), 'g', 'LineWidth', 1.5, 'DisplayName', 'rcy, n=3');

xlabel('Real part of z');
ylabel('rcy');
title('Riccati-Bessel function (rcy) for z from 0 to 14');
ylim([-2 +2]);
legend('Location', 'best');
grid on;
