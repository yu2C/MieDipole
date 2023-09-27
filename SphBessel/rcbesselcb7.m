% Define the range for z (real and imaginary parts)
real_parts = linspace(-2, 2, 100);
imaginary_parts = linspace(-2, 2, 100);
[real_mesh, imag_mesh] = meshgrid(real_parts, imaginary_parts);

% Combine real and imaginary parts to create complex z values
z_values = complex(real_mesh, imag_mesh);

% Calculate rcj for z = -2-2i to +2+2i and n = 2
n = 2;
rcj_values = zeros(size(z_values));
for i = 1:numel(z_values)
    [~, ~, ~, drcy] = rcbesselc(z_values(i), n);
    rcj_values(i) = drcy(n + 1);  % Use drcy as rcj is not defined in the provided code
end

% Reshape the results to match the grid
rcj_values = reshape(rcj_values, size(real_mesh));

% Create a 3D plot
figure;
surf(real_mesh, imag_mesh, real(rcj_values), imag(rcj_values), 'EdgeColor', 'interp');
xlabel('Real part of z');
ylabel('Imaginary part of z');
zlabel('Real part of rcj');
title('3D Plot of rcj for z = -2-2i to +2+2i (n = 2)');
colorbar;
zlim([-1.5 +1.5])
% Rotate the plot for better visualization
view(-30, 30);
