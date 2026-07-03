% Define the range of real values for z
z_values = linspace(0, 14, 1000);

% Initialize arrays for drcy values for different n values
n_values = [1, 2, 3];
drcy_values = zeros(length(n_values), length(z_values));

% Calculate drcy for each n and each real value of z
for i = 1:length(n_values)
    n = n_values(i);
    for j = 1:length(z_values)
        z = complex(z_values(j), 0);  % Imaginary part is 0 for this case
        [~, ~, ~, drcy] = rcbesselc(z, n);
        drcy_values(i, j) = drcy(n + 1);  % MATLAB uses 1-based indexing
    end
end

% Plot drcy for different n values as a function of the real part of z
figure;
plot(z_values, real(drcy_values));
xlabel('Real part of z');
ylabel('drcy');
title('Derivative of Riccati-Bessel function (drcy) for z from 0 to 14');
ylim([-2 +2])
legend('n = 1', 'n = 2', 'n = 3');
grid on;
