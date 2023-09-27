% Values for the plot
z_values = linspace(-2-2i, 2+2i, 100);  % Modify the range and number of points as needed
rcj_real_values = zeros(size(z_values));
rcj_imag_values = zeros(size(z_values));

% Generate rcj for each z value and collect real and imaginary parts
for i = 1:length(z_values)
    z_value = z_values(i);
    [rcj, ~, ~, ~] = rcbesselc(z_value, 1);
    rcj_real_values(i) = real(rcj(2));
    rcj_imag_values(i) = imag(rcj(2));
end

% Plot
figure;
plot(real(z_values), rcj_real_values, 'b', 'DisplayName', 'Re(rcj) for n=1');
hold on;
plot(real(z_values), rcj_imag_values, 'r', 'DisplayName', 'Im(rcj) for n=1');
xlabel('Re(z)');
ylabel('Values');
legend;
title('Re(rcj) and Im(rcj) for n=1');
