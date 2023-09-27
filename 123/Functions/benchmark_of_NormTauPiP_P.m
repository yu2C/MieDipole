% Assuming struct1 and struct2 have arrays NP, NTau, and NPi
subtracted_struct.NP = NTau_pyvalues - NTau_values;
%subtracted_struct.NTau = ans.NTau - NTau;
%subtracted_struct.NPi = ans.NPi - NPi;

% Plot NP from the subtracted struct
figure;
plot(subtracted_struct.NP);
title('NTau(nmax = 1)');
xlabel('theta(e-2)');
ylabel('NTau');
ylim([-5*10^-14 +5*10^-14])
xlim([0 650])

