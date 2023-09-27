% Define the range for kr (real and imaginary parts)
kr_real_parts = linspace(-2, 2, 100);
kr_imaginary_parts = linspace(-2, 2, 100);
[kr_real_mesh, kr_imag_mesh] = meshgrid(kr_real_parts, kr_imaginary_parts);
kr_values = kr_real_mesh + 1i * kr_imag_mesh;

% Initialize an array to store the derivative of Z (dpsi)
dpsi_values = zeros(size(kr_values));

% Calculate dpsi for kr = -2-2i to +2+2i and nmax = 2, array = 1, type = 'bessel'
nmax = 2;
array = 1;
type = 'bessel';

for i = 1:numel(kr_values)
    kr = kr_values(i);
    result = SphBessel(kr, nmax, array, type);
    dpsi_values(i) = result.dpsi(nmax);  % Extract the derivative of Z
end

% Reshape the results to match the grid
dpsi_values = reshape(dpsi_values, size(kr_real_mesh));

% Create a 3D plot
figure;
surf(kr_real_mesh, kr_imag_mesh, real(dpsi_values));
colorbar;
xlabel('Real part of kr');
ylabel('Imaginary part of kr');
zlabel('Real part of dpsi');
title('3D Plot of real part of dpsi for kr = -2-2i to +2+2i (nmax = 2, array = 1, type = ''bessel'')');
