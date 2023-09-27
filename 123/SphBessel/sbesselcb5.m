% Define the range of complex values for z
real_values = linspace(-2, 2, 100);
imag_values = linspace(-2, 2, 100);
[z_real, z_imag] = meshgrid(real_values, imag_values);
z_values = z_real + 1i * z_imag;

% Calculate csy for n=2 for each complex z
n = 2;
csy_values = zeros(size(z_values));
for i = 1:size(z_values, 1)
    for j = 1:size(z_values, 2)
        [~, csy] = sbesselc(z_values(i, j), n);
        csy_values(i, j) = csy(n + 1);
    end
end

% Plot the 3D surface
figure;
surf(z_real, z_imag, abs(csy_values), 'EdgeColor', 'none');
xlabel('Real part of z');
ylabel('Imaginary part of z');
zlabel(['|csy(z, n=' num2str(n) ')']);
title(['csy(z, n=' num2str(n) ') for z = -2-2i to +2+2i']);
axis tight;
view(20, -45);
colorbar;

% Adjust z-axis limits
zlim([0, max(abs(csy_values(:)))]);
