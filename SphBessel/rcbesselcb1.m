% Define the range of real values for z
z_values = linspace(0, 14, 100);

% Initialize arrays for rcj values for different n values
n_values = [0, 1, 2, 3];
rcj_values = zeros(length(n_values), length(z_values));

% Calculate rcj for each n and each real value of z
for i = 1:numel(n_values)
    n = n_values(i);
    for j = 1:numel(z_values)
        z = complex(z_values(j), 0);  % Imaginary part is 0 for this case
        [rcj, ~, ~, ~] = rcbesselc(z, n);
        rcj_values(i, j) = rcj(n + 1);  % MATLAB uses 1-based indexing
    end
end

% Plot rcj for different n values as a function of z
figure;
plot(z_values, real(rcj_values(1, :)), 'b-', 'LineWidth', 1.5, 'DisplayName', 'n=0');
hold on;
plot(z_values, real(rcj_values(2, :)), 'r--', 'LineWidth', 1.5, 'DisplayName', 'n=1');
plot(z_values, real(rcj_values(3, :)), 'g:', 'LineWidth', 1.5, 'DisplayName', 'n=2');
plot(z_values, real(rcj_values(4, :)), 'm-.', 'LineWidth', 1.5, 'DisplayName', 'n=3');
xlabel('Real part of z');
ylabel('rcj');
title('rcj for z from 0 to 14, n=0 to 3');
legend('Location', 'best');
grid on;
hold off;
