% Define the range for z (real and imaginary parts)
real_parts = linspace(-2, 2, 100);
imaginary_parts = linspace(-2, 2, 100);
[real_mesh, imag_mesh] = meshgrid(real_parts, imaginary_parts);

% Combine real and imaginary parts to create complex z values
z_values = real_mesh + 1i * imag_mesh;

% Initialize an array to store drcj values
drcj_values = zeros(size(z_values));

% Calculate drcj for z = -2-2i to +2+2i and n = 2
n = 2;
for i = 1:numel(z_values)
    [~, ~, drcj, ~] = rcbesselc(z_values(i), n);
    drcj_values(i) = drcj(n + 1);  % drcj is 0-indexed, so we use n + 1
end

% Reshape the results to match the grid
drcj_values = reshape(drcj_values, size(real_mesh));

% Create a 3D plot
figure;
surf(real_mesh, imag_mesh, real(drcj_values));  % Plot the real part of drcj
colorbar;  % Add a colorbar

xlabel('Real part of z');
ylabel('Imaginary part of z');
zlabel('Real part of drcj');
title('3D Plot of drcj for z = -2-2i to +2+2i (n = 2)');
