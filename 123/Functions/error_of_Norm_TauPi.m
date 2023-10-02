% Define the range of x (indn)
x = 1:100;

% Compute y for each x
y = sqrt((2*x + 1) ./ (2*x .* (x + 1)));


% Plot the values
plot(x, y);
%xlabel('indn');
xlabel('$$\mathrm{n}$$','interpreter','latex', 'FontSize', 18);

%ylabel('y');
ylabel('$$\mathrm{y}$$','interpreter','latex', 'FontSize', 18);

%title('Plot of y = sqrt((2*indn+1)/8) for x = 0 to 100');
title('$$\mathrm{y}=\sqrt{\frac{2\mathrm{n}+1}{2\mathrm{n}(\mathrm{n}+1)}}~\mathrm{v.s.}~\mathrm{n}$$','Interpreter', 'latex', 'FontName', 'Times New Roman', 'FontSize', 22);

xlim = ([0 100]);
%ylim = ([0 5.5]);
ylim = ([0 1.0]);
yticks([0.1,  0.3,  0.5,  0.7,  0.9]);  % Adjust these values accordingly


ax = gca;
ax.XAxis.FontSize = 15;
ax.YAxis.FontSize = 15;
