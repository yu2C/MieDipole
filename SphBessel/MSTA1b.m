%% Sub-Functions of Spherical Bessel/Riccati-Bessel Functions
% Ref: Computation of Special Functions (1996)
%        Authors: Shanjie Zhang, Jianming Jin
%----------------------------------------------
% Called by sbesselc.m and rcbesselc.m



% Define z values ranging from 1 to 10
z_values = 1:1:10;

% Fixed mp value
mp = 200;

% Initialize an array to store MSTA1 values
MSTA1_values = zeros(size(z_values));

% Calculate MSTA1(z, mp) values for each z
for i = 1:length(z_values)
    MSTA1_values(i) = MSTA1(z_values(i), mp);
end

% Create the plot
plot(z_values, MSTA1_values)
xlabel('z')
ylabel('MSTA1(z, mp)')
title('MSTA1(z, mp) for mp=200')
grid on

