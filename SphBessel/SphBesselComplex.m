function Rad = SphBesselComplex(kr, nmax, array, type)
    z1 = zeros(1, nmax);
    Z = zeros(1, nmax);
    dZ = zeros(1, nmax);
    raddZ = zeros(1, nmax);
    
    for i = 1:numel(kr)
        kri = kr(i);
        [csj, ~] = sbesselc(kri, nmax);
        if array == 1
            z1(i, :) = csj(2:nmax+1);
        else
            z1(i, :) = csj(nmax+1);
        end

        % Riccati-Bessel Functions and their Derivatives
        [rcj, ~, drcj, ~] = rcbesselc(kri, nmax);
        if array == 0
            Z(i, :) = rcj(nmax+1);
            dZ(i, :) = drcj(nmax+1);
            raddZ(i, :) = dZ(i, :)./kri;
        else
            rcj(1) = [];
            drcj(1) = [];
            Z(i, :) = rcj;
            dZ(i, :) = drcj;
            raddZ(i, :) = dZ(i, :)./kri;
        end
    end

    Rad.j1 = z1;
    Rad.psi = Z;
    Rad.dpsi = dZ;
    Rad.raddpsi = raddZ;
end

