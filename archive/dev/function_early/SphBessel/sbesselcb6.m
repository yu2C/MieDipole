% Define the range of real values for z
z_values = linspace(1, 14, 130);

% Initialize arrays for csy values for different n values
n_values = [1, 2, 3];
csy_values = zeros(length(n_values), length(z_values));

% Calculate csy for each n and each real value of z
for i = 1:length(n_values)
    n = n_values(i);
    for j = 1:length(z_values)
        z = complex(z_values(j), 0);  % Imaginary part is 0 for this case
        [~, csy] = sbesselc(z, n);
        csy_values(i, j) = csy(n + 1);  % MATLAB uses 1-based indexing
    end
end

% Plot csy for different n values as a function of z
figure;
plot(z_values, real(csy_values(1, :)), 'b-', 'LineWidth', 1.5, 'DisplayName', 'n=1');
hold on;
plot(z_values, real(csy_values(2, :)), 'r--', 'LineWidth', 1.5, 'DisplayName', 'n=2');
plot(z_values, real(csy_values(3, :)), 'g-.', 'LineWidth', 1.5, 'DisplayName', 'n=3');

xlabel('Real part of z');
ylabel('csy');
title('csy for z from 1 to 14 for n=1 to 3');
legend('Location', 'best');
grid on;
xlim([1, 14]);  % Fix x-axis from 2 to 14
ylim([-0.4, 0.4])
hold off;
