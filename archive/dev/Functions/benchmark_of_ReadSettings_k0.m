% Assuming struct1 and struct2 have arrays NP, NTau, and NPi
subtracted_struct.NP = ans.Settings.k0 - Settings_py.k0';
%subtracted_struct.NTau = ans.NTau - NTau;
%subtracted_struct.NPi = ans.NPi - NPi;

% Plot NP from the subtracted struct
figure;
plot(subtracted_struct.NP);
%title('\fontsize{16}wavenumber k_0');
title('wavenumber k_0', 'FontName', 'Times New Roman', 'FontSize', 16);

xticks([0, 100, 200, 300, 400]);  % Adjust these values accordingly
xticklabels({'2.09', '1.57', '1.26', '1.05', '0.898'});  % Labels for the ticks


ylim([-5e-16, +5e-16]);
xlim([0, 401]);
%xlabel('\fontsize{11}300-700 nm');
xlabel('2.09-0.898 cm^{-1}', 'FontName', 'Times New Roman', 'FontSize', 13);

%ylabel('\fontsize{11}Absolute Error');
ylabel('Absolute Error', 'FontName', 'Times New Roman', 'FontSize', 13);
