% Define the range for z (real and imaginary parts)
real_parts = linspace(2, 15, 100);
imaginary_parts = linspace(2, 15, 100);
[real_mesh, imag_mesh] = meshgrid(real_parts, imaginary_parts);
z_values = real_mesh + 1i * imag_mesh;

% Initialize an array to store drcy values
drcy_values = zeros(size(z_values));

% Calculate drcy for z = 2+2i to 15+15i and n = 2
n = 2;
for i = 1:numel(z_values)
    [~, ~, ~, drcy] = rcbesselc(z_values(i), n);
    drcy_values(i) = drcy(n);
end

% Reshape the results to match the grid
drcy_values = reshape(drcy_values, size(real_mesh));

% Create a 3D plot
figure;
surf(real_mesh, imag_mesh, real(drcy_values));
colorbar;
xlabel('Real part of z');
ylabel('Imaginary part of z');
zlabel('Real part of drcy');
title('3D Plot of drcy for z = 2+2i to 15+15i (n = 2)');
