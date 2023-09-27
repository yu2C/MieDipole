function NTau_values = benchmark_of_NormTauPiP(nmax, theta_range, type)
    % Initialize NP_values as an empty array
    NTau_values = [];

    for theta = theta_range
        % Compute normalized vector spherical harmonics array for each theta
        NAng = NormTauPiP(nmax, theta, type);
        
        % Extract NP values for this theta and flatten into a row vector
        NTau_theta = NAng.NTau(:)';
        
        % Append the row vector to NP_values
        NTau_values = [NTau_values; NTau_theta];
    end
end

% Example usage
%nmax = 1;
%theta_range = linspace(0, 2*pi, 628);  % Adjust the number of points as needed
%type = 'normal';
%NP_values = benchmark_of_NormTauPiP(nmax, theta_range, type);

% Display the size of NP_values
%disp(['Size of NP_values: ', num2str(size(NP_values))]);

