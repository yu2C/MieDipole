% Define the range of real values for z
z_values = linspace(0, 14, 100);

% Initialize arrays for drcj values for different n values
n_values = [1, 2, 3];
drcj_values = zeros(length(n_values), length(z_values));

% Calculate drcj for each n and each real value of z
for i = 1:length(n_values)
    n = n_values(i);
    for j = 1:length(z_values)
        z = complex(z_values(j), 0);  % Imaginary part is 0 for this case
        [~, ~, drcj, ~] = rcbesselc(z, n);
        drcj_values(i, j) = drcj(n + 1);  % MATLAB uses 1-based indexing
    end
end

% Plot drcj for different n values as a function of the real part of z
figure;
for i = 1:length(n_values)
    plot(z_values, real(drcj_values(i, :)), 'LineWidth', 1.5, 'DisplayName', ['n = ', num2str(n_values(i))]);
    hold on;
end

xlabel('Real part of z');
ylabel('drcj');
title('Derivative of Riccati-Bessel function (drcj) for z from 0 to 14');
legend('Location', 'best');
grid on;
hold off;
