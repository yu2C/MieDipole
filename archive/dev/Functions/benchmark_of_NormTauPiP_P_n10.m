% Define nmax and number of points
nmax = 50;
num_points = 628;

% Initialize an array to store the results
result_array = zeros(num_points, 2 * nmax + 1);

% Generate theta values
theta_values = linspace(0, 2*pi, num_points);

% Loop to compute and store the NTau values
for i = 1:num_points
    theta = theta_values(i);
    NAng = NormTauPiP(nmax, theta, 'normal');
    result_array(i, :) = NAng.NP(1, :);
end

% Display a message
disp('NPi values computed and stored in the result_array.');

% Now you can use the result_array in MATLAB as needed.
% For example, to plot the values:
%x = 0:2*nmax;
%plot(x, result_array.');
