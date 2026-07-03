% Assuming struct1 and struct2 have arrays NP, NTau, and NPi
subtracted_struct.NP = ans.NP - NP;
subtracted_struct.NTau = ans.NTau - NTau;
subtracted_struct.NPi = ans.NPi - NPi;

% Plot NP from the subtracted struct
figure;
plot(subtracted_struct.NP);
title('Subtracted NP');
xlabel('Index');
ylabel('Value');

