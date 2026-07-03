% Define the range of complex values for z
real_values = linspace(-2, 2, 100);
imag_values = linspace(-2, 2, 100);
[z_real, z_imag] = meshgrid(real_values, imag_values);
z_values = z_real + 1i * z_imag;

% Compute MSTA1 for each complex z
msta_values = zeros(size(z_values));
for i = 1:size(z_values, 1)
    for j = 1:size(z_values, 2)
        msta_values(i, j) = MSTA1(z_values(i, j), 200);
    end
end

% Plot the 3D surface
figure;
surf(z_real, z_imag, msta_values);
xlabel('Real part of z');
ylabel('Imaginary part of z');
zlabel('MSTA1(z, 200)');
title('MSTA1(z, 200) for z = -2-2i to +2+2i');
