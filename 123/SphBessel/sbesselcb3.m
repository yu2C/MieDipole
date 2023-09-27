% Define the range of real values for z
z_values = linspace(0, 14, 140);

% Initialize arrays for csj values for different n values
n_values = [1, 2, 3];
csj_values = zeros(numel(z_values), numel(n_values));

% Calculate csj for each n and each real value of z
for j = 1:numel(n_values)
    n = n_values(j);
    for i = 1:numel(z_values)
        z = complex(z_values(i), 0);  % Imaginary part is 0 for this case
        [csj, ~] = sbesselc(z, n);
        csj_values(i, j) = csj(n + 1);  % MATLAB uses 1-based indexing
    end
end

% Print the csj values
disp('csj values for z from 0 to 14:')
disp(csj_values)

% Plot csj for different n values as a function of the real part of z
figure;
plot(z_values, csj_values, 'LineWidth', 1.5);
xlabel('Real part of z');
ylabel('csj');
title('csj for z from 0 to 14 for n=1 to 3');
legend('n=1', 'n=2', 'n=3');
grid on;
axis([0 14 -0.5 1.0]);  % Fix x-axis from 0 to 14
