% Assuming struct1 and struct2 have arrays NP, NTau, and NPi
VSF_M_reshaped = reshape(VSF.N, [], 1);
VSFpy_M_reshaped = reshape(VSFpy.N, [], 1);

subtracted_struct.NP = VSF_M_reshaped - VSFpy_M_reshaped;
%subtracted_struct.NTau = ans.NTau - NTau;
%subtracted_struct.NPi = ans.NPi - NPi;
%asubtracted_struct.NP = ans.Settings.nr(1,2) - Settings_py.nr(1,2);
x = 1:29610;

% Plot NP from the subtracted struct
figure;
plot(x, abs(subtracted_struct.NP));
%title('\fontsize{16}wavenumber k_0');
title('$$\mathrm{VSF.N}$$','Interpreter', 'latex', 'FontName', 'Times New Roman', 'FontSize', 22);

%xticks([0, 100, 200, 300, 400]);  % Adjust these values accordingly
%xticklabels({'2.09', '1.57', '1.26', '1.05', '0.898'});  % Labels for the ticks


%ylim([-3e-13, +3e-13]);
%xlim([0, 401]);
%xlabel('\fontsize{11}300-700 nm');
%xlabel('$$300-700~\mathrm{nm}$$','interpreter','latex', 'FontName', 'Times New Roman', 'FontSize', 13);
xlabel('$$\mathrm{label}$$','interpreter','latex', 'FontSize', 18);


%ylabel('\fontsize{11}Absolute Error');
%ylabel('$$\mathrm{absolute~error}$$','interpreter','latex', 'FontName', 'Times New Roman', 'FontSize', 13);
ylabel('$$\mathrm{absolute~error}$$','interpreter','latex', 'FontSize', 18);

ax = gca;
ax.XAxis.FontSize = 15;
ax.YAxis.FontSize = 15;
