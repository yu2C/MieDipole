% Define the range of n values
n_values = 2:50;

% Fixed complex value for z
z = 2 + 2i;

% Calculate MSTA2 for each n
mp = 15;
msta2_values = arrayfun(@(n) MSTA2(z, n, mp), n_values);

% Plot the values
figure;
plot(n_values, msta2_values, 'o-');
xlabel('n');
ylabel(['MSTA2(z=' num2str(z) ', n, mp=' num2str(mp) ')']);
title(['MSTA2(z=' num2str(z) ', n, mp=' num2str(mp) ') for n=2 to 50']);
grid on;
