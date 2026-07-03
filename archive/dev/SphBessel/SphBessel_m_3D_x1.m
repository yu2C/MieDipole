% Define the range for kr (real and imaginary parts)
kr_real_parts = linspace(-2, 2, 100);
kr_imaginary_parts = linspace(-2, 2, 100);
[kr_real_mesh, kr_imag_mesh] = meshgrid(kr_real_parts, kr_imaginary_parts);
kr_values = kr_real_mesh + 1i * kr_imag_mesh;

% Initialize an array to store x1 values
x1_values = zeros(size(kr_values));

% Calculate x1 for kr = -2-2i to +2+2i and nmax = 2, array = 1, type = 'hankel1'
nmax = 2;
array = 1;
type = 'hankel1';

for i = 1:numel(kr_values)
    kr = kr_values(i);
    result = SphBessel(kr, nmax, array, type);
    x1_values(i) = result.h1(nmax);  % Extract x1
end

% Reshape the results to match the grid
x1_values = reshape(x1_values, size(kr_real_mesh));

% Create a 3D plot for x1
figure;
surf(kr_real_mesh, kr_imag_mesh, real(x1_values));
colorbar;
xlabel('Real part of kr');
ylabel('Imaginary part of kr');
zlabel('Real part of x1');
title('3D Plot of real part of x1 for kr = -2-2i to +2+2i (nmax = 2, array = 1, type = ''hankel1'')');
