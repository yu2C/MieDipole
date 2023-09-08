j = 1.5;
theta = 0;

%function d = Wigner_d(j, theta)
    % Calculation of J+
    m = -j: j-1;
    J = diag(sqrt((j-m).*(j+m+1)), -1);
    % Create the Spectral Decomposition Matrix J_y at z Representation
    Jy = (J-J')/2i;
    % Diagonalization
    [V, D] = eig(Jy);
    %check the eigenvalue problem
    E = V*D*V';
    % Unitary Transformation
    G = exp(-1i*theta*diag(D));
    d = V*diag(G)*V';
    % Check the Quality of the Transformation
    %if max(max(abs(imag(d)))) > 1e-12
     %   warn_mes = 'Wigner_d may not give reliable results.';
      %  dispstat(sprintf(warn_mes),'keepthis','timestamp');
   % end
    % Change Data Type (double complex -> double real)
    d = real(d);
%end

