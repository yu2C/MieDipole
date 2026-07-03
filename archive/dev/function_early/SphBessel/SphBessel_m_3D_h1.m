% Define the range for kr (real and imaginary parts)
kr_real_parts = linspace(-2, 2, 100);
kr_imaginary_parts = linspace(-2, 2, 100);
[kr_real_mesh, kr_imag_mesh] = meshgrid(kr_real_parts, kr_imaginary_parts);
kr_values = kr_real_mesh + 1i * kr_imag_mesh;

% Initialize an array to store h1 values
h1_values = zeros(size(kr_values));

% Calculate h1 for kr = -2-2i to +2+2i and nmax = 2, array = 1, type = 'hankel1'
nmax = 2;
array = 1;
type = 'hankel1';

for i = 1:numel(kr_values)
    kr = kr_values(i);
    result = SphBessel(kr, nmax, array, type);
    h1_values(i) = result.h1(nmax);  % Extract h1
end

% Reshape the results to match the grid
h1_values = reshape(h1_values, size(kr_real_mesh));

% Create a 3D plot for h1
figure;
surf(kr_real_mesh, kr_imag_mesh, real(h1_values));
colorbar;
xlabel('Real part of kr');
ylabel('Imaginary part of kr');
zlabel('Real part of h1');
title('3D Plot of real part of h1 for kr = -2-2i to +2+2i (nmax = 2, array = 1, type = ''hankel1'')');
