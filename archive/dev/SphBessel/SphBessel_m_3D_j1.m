% Define the range for kr (real and imaginary parts)
kr_real_parts = linspace(-2, 2, 100);
kr_imaginary_parts = linspace(-2, 2, 100);
[kr_real_mesh, kr_imag_mesh] = meshgrid(kr_real_parts, kr_imaginary_parts);
kr_values = kr_real_mesh + 1i * kr_imag_mesh;

% Initialize an array to store the real part of j1
j1_real_values = zeros(size(kr_values));

% Calculate j1 for kr = -2-2i to +2+2i and nmax = 2, array = 1, type = 'bessel'
nmax = 2;
array = 1;
type = 'bessel';

for i = 1:numel(kr_values)
    kr = kr_values(i);
    result = SphBessel(kr, nmax, array, type);
    j1_real_values(i) = real(result.j1(nmax));  % Extract the real part of j1
end

% Reshape the results to match the grid
j1_real_values = reshape(j1_real_values, size(kr_real_mesh));

% Create a 3D plot
figure;
surf(kr_real_mesh, kr_imag_mesh, (j1_real_values-j1_real_valuespy));
colorbar;
%xlabel('Real part of kr');
xlabel('$$\mathrm{Re(kr)}$$','interpreter','latex', 'FontSize', 18);

%ylabel('Imaginary part of kr');
ylabel('$$\mathrm{Im(kr)}$$','interpreter','latex', 'FontSize', 18);

%zlabel('Real part of j1');
zlabel('$$\mathrm{absolute~error}$$','interpreter','latex', 'FontSize', 18);

%title('3D Plot of real part of j1 for kr = -2-2i to +2+2i (nmax = 2, array = 1, type = ''bessel'')');
title('$$\mathrm{j1}~\mathrm{for}~\mathrm{kr}=-2-2i~\mathrm{to}~+2+2i~$$', '$$(\mathrm{nmax}=2,~\mathrm{array}=1,~\mathrm{type}=\mathrm{bessel})$$', 'Interpreter', 'latex', 'FontName', 'Times New Roman', 'FontSize', 22);
zlim([-2e-13, 2e-13]);

ax = gca;
ax.XAxis.FontSize = 15;
ax.YAxis.FontSize = 15;
ax.ZAxis.FontSize = 15;

