% Define the range of x (indn)
x = 0:100;

% Compute y for each x
y = sqrt((2*x + 1) / 8);

% Plot the values
plot(x, y);
%xlabel('indn');
xlabel('$$\mathrm{n}$$','interpreter','latex', 'FontSize', 18);

%ylabel('y');
ylabel('$$\mathrm{y}$$','interpreter','latex', 'FontSize', 18);

%title('Plot of y = sqrt((2*indn+1)/8) for x = 0 to 100');
title('$$\mathrm{y}=\sqrt{\frac{2\mathrm{n}+1}{8}}~\mathrm{v.s.}~\mathrm{n}$$','Interpreter', 'latex', 'FontName', 'Times New Roman', 'FontSize', 22);

xlim = ([0 100]);
ylim = ([0 5.5]);

ax = gca;
ax.XAxis.FontSize = 15;
ax.YAxis.FontSize = 15;
