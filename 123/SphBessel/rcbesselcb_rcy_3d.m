% Define the range for z (real and imaginary parts)
real_parts = linspace(-2, 2, 100);
imaginary_parts = linspace(-2, 2, 100);
[real_mesh, imag_mesh] = meshgrid(real_parts, imaginary_parts);
z_values = real_mesh + 1i * imag_mesh;

% Initialize an array to store rcy values
rcy_values = zeros(size(z_values));

% Calculate rcy for z = -2-2i to +2+2i and n = 2
n = 2;
for i = 1:numel(z_values)
    [~, rcy, ~, ~] = rcbesselc(z_values(i), n);
    rcy_values(i) = rcy(n);
end

% Reshape the results to match the grid
rcy_values = reshape(rcy_values, size(real_mesh));

% Create a 3D plot
figure;
surf(real_mesh, imag_mesh, real(rcy_values));
colorbar;
xlabel('Real part of z');
ylabel('Imaginary part of z');
zlabel('Real part of rcy');
title('3D Plot of rcy for z = -2-2i to +2+2i (n = 2)');
