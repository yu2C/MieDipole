% Assuming struct1 and struct2 have arrays NP, NTau, and NPi
subtracted_struct.NP = ans.Settings.lambda - Settings_py.lambda';
%subtracted_struct.NTau = ans.NTau - NTau;
%subtracted_struct.NPi = ans.NPi - NPi;

% Plot NP from the subtracted struct
figure;
plot(subtracted_struct.NP);
title('$$\mathrm{wavelength}~\lambda$$','Interpreter', 'latex', 'FontSize', 22);


xticks([0, 100, 200, 300, 400]);  % Adjust these values accordingly
xticklabels({'300', '400', '500', '600', '700'});  % Labels for the ticks


ylim([-5e-15, +5e-15]);
xlim([0, 401]);
%xlabel('\fontsize{13}300-700 nm');
xlabel('$$\mathrm{values}~(\mathrm{nm})$$','interpreter','latex', 'FontSize', 18);

%ylabel('Absolute Error');
ylabel('$$\mathrm{absolute~error}$$','interpreter','latex', 'FontSize', 18);

ax = gca;
ax.XAxis.FontSize = 15;
ax.YAxis.FontSize = 15;

