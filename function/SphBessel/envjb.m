%% Sub-Functions of MSTA1/MSTA2
% Ref: Computation of Special Functions (1996)
%        Authors: Shanjie Zhang, Jianming Jin
%----------------------------------------------
% Called by MSTA1.m and MSTA2.m



% Define z values ranging from 1 to 10
z = 1:0.001:50;

% Define values of n
n_values = 1:9;

% Initialize an array to store envj(n, z) values for each n
envj_values = zeros(length(n_values), length(z));

% Calculate envj(n, z) values for each n and z
for i = 1:length(n_values)
    n = n_values(i);
    for j = 1:length(z)
        envj_values(i, j) = envj(n, z(j));
    end
end

% Create the plot with multiple lines
figure
hold on
for i = 1:length(n_values)
    plot(z, envj_values(i, :), 'DisplayName', ['n = ', num2str(n_values(i))])
end
hold off

xlabel('z')
ylabel('envj(n, z)')
title('envj(n, z) for n = 1, 2, 3')
legend('Location', 'Best')
grid on
