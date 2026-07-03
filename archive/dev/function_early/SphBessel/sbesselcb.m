% Define z and n values
z = 4 + 2i;
n_values = [2, 3, 10];

% Print csj values for each n
for n = n_values
    [csj, ~] = sbesselc(z, n);
    fprintf('csj(z=%d+%di, n=%d) = %f + %fi\n', real(z), imag(z), n, real(csj(n+1)), imag(csj(n+1)));
end
