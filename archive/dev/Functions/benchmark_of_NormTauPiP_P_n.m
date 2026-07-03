% Parameters
theta = pi/4;
order = 'normal';

% Initialize a cell array to store NP values
NP_cell = cell(50, 1);

for nmax = 1:50
    % Compute NP values
    NAng = NormTauPiP(nmax, theta, order);
    
    % Store NP values in the cell array
    NP_cell{nmax} = NAng.NP;
end

% Save the cell array to a .mat file
save('NP_values.mat', 'NP_cell');

disp('NP values have been saved to NP_values.mat.');
