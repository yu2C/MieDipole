% Define the range for kr (real and imaginary parts)
kr_real_parts = linspace(-2, 2, 100);
kr_imaginary_parts = linspace(-2, 2, 100);
[kr_real_mesh, kr_imag_mesh] = meshgrid(kr_real_parts, kr_imaginary_parts);
kr_values = kr_real_mesh + 1i * kr_imag_mesh;

% Initialize an array to store raddpsi values
raddpsi_values = zeros(size(kr_values));

% Calculate raddpsi for kr = -2-2i to +2+2i and nmax = 2, array = 1, type = 'bessel'
nmax = 2;
array = 1;
type = 'bessel';

for i = 1:numel(kr_values)
    kr = kr_values(i);
    result = SphBessel(kr, nmax, array, type);
    raddpsi_values(i) = result.raddpsi(nmax);  % Extract raddpsi
end

% Reshape the results to match the grid
raddpsi_values = reshape(raddpsi_values, size(kr_real_mesh));

% Create a 3D plot for raddpsi
figure;
surf(kr_real_mesh, kr_imag_mesh, real(raddpsi_values));
colorbar;
xlabel('Real part of kr');
ylabel('Imaginary part of kr');
zlabel('Real part of raddpsi');
title('3D Plot of real part of raddpsi for kr = -2-2i to +2+2i (nmax = 2, array = 1, type = ''bessel'')');
