% Define the complex z values
z_real = linspace(-2, 2, 5);
z_imag = linspace(-2, 2, 5) * 1i;
[z_real_grid, z_imag_grid] = meshgrid(z_real, z_imag);
z_values = z_real_grid + z_imag_grid;

% Initialize arrays to store real and imaginary parts of rcj
rcj_real = zeros(size(z_values));
rcj_imag = zeros(size(z_values));

% Calculate the rcj values for n=1
n = 1;
for i = 1:numel(z_values)
    [rcj, ~, ~, ~] = rcbesselc(z_values(i), n);
    rcj_real(i) = real(rcj(1));
    rcj_imag(i) = imag(rcj(1));
end

% Plot the real and imaginary parts of rcj
figure;
scatter(rcj_real(:), rcj_imag(:), 'b.');
title('Plot of rcj with z from -2-2i to +2+2i (n=1)');
xlabel('Real(rcj)');
ylabel('Imag(rcj)');
grid on;

% Save the plot as an image
saveas(gcf, 'rcj_plot_matlab.png');
