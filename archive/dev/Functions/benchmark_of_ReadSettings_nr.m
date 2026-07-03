% Assuming struct1 and struct2 have arrays NP, NTau, and NPi
subtracted_struct.NP = imag(ans.Settings.nr(:,2)) - imag(Settings_py.nr(:,2));
%subtracted_struct.NTau = ans.NTau - NTau;
%subtracted_struct.NPi = ans.NPi - NPi;
%asubtracted_struct.NP = ans.Settings.nr(1,2) - Settings_py.nr(1,2);

% Plot NP from the subtracted struct
figure;
plot(subtracted_struct.NP);
%title('\fontsize{16}wavenumber k_0');
title('$$\mathrm{refraction~index}~\mathrm{Im}(n_{r})$$','Interpreter', 'latex', 'FontName', 'Times New Roman', 'FontSize', 22);

xticks([0, 100, 200, 300, 400]);  % Adjust these values accordingly
xticklabels({'0.9903', '2.0916', '3.1210', '4.0024', '4.7949'});  % Labels for the ticks


ylim([-5e-15, +5e-15]);
xlim([0, 401]);
%xlabel('\fontsize{11}300-700 nm');
%xlabel('$$300-700~\mathrm{nm}$$','interpreter','latex', 'FontName', 'Times New Roman', 'FontSize', 13);
xlabel('$$\mathrm{values}$$','interpreter','latex', 'FontSize', 18);


%ylabel('\fontsize{11}Absolute Error');
%ylabel('$$\mathrm{absolute~error}$$','interpreter','latex', 'FontName', 'Times New Roman', 'FontSize', 13);
ylabel('$$\mathrm{absolute~error}$$','interpreter','latex', 'FontSize', 18);

ax = gca;
ax.XAxis.FontSize = 15;
ax.YAxis.FontSize = 15;
