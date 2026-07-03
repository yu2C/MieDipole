% Define the range of complex values for z
real_values = linspace(-2, 2, 100);
imag_values = linspace(-2, 2, 100);
[z_real, z_imag] = meshgrid(real_values, imag_values);
z_values = z_real + 1i * z_imag;

% Calculate MSTA2 with n=2 and mp=15 for each complex z
n = 2;
mp = 15;
msta2_values = zeros(size(z_values));

for i = 1:numel(z_values)
    msta2_values(i) = MSTA2(z_values(i), n, mp);
end

% Reshape for plotting
msta2_values = reshape(msta2_values, size(z_real));

% Plot the 3D surface
figure;
surf(z_real, z_imag, msta2_values);
xlabel('Real part of z');
ylabel('Imaginary part of z');
zlabel(['MSTA2(z, n=' num2str(n) ', mp=' num2str(mp) ')']);
title(['MSTA2(z, n=' num2str(n) ', mp=' num2str(mp) ') for z = -2-2i to +2+2i']);
